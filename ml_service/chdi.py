import numpy as np
from scipy.spatial.distance import mahalanobis
from typing import List, Dict, Tuple, Optional
from ml_service.models import (
    ObservationVector,
    HistoricalObservation,
    CHDIComputeRequest,
    CHDIComputeResponse,
    FactorAttribution
)

# IEEE Paper Section IV Mathematical Constants
DEFAULT_WINDOW_SIZE = 14          # W = 14 observations
TIKHONOV_LAMBDA = 1e-3            # Regularization ridge lambda = 10^-3
D_MAX = 4.0                       # Maximum distance boundary (4.0 sigma)
N_SATURATION = 14                 # Baseline saturation constant
EPSILON = 1e-4                    # Numerical guard against division by zero

SIGNAL_NAMES = ["milk", "rumination", "temperature", "activity", "feed", "weight"]

HUMAN_LABELS = {
    "milk": "Daily Milk Yield",
    "rumination": "Rumination Duration",
    "temperature": "Core Body Temperature",
    "activity": "Physical Activity",
    "feed": "Feed Intake",
    "weight": "Body Weight"
}

def extract_signal_array(obs: ObservationVector, signals: List[str]) -> List[Optional[float]]:
    res = []
    for s in signals:
        res.append(getattr(obs, s, None))
    return res

def compute_stage1_baseline(
    history: List[HistoricalObservation],
    signal: str,
    window: int = DEFAULT_WINDOW_SIZE
) -> Tuple[float, float, int]:
    """
    Stage 1 — Equation (1) & (2): Rolling moving-average baseline and sample variance with Bessel's correction.
    """
    vals = [getattr(h, signal) for h in history if getattr(h, signal, None) is not None]
    if not vals:
        return 0.0, 1.0, 0
    
    recent = vals[-window:]
    mean = float(np.mean(recent))
    if len(recent) > 1:
        # Bessel's correction (W - 1)
        std = float(np.std(recent, ddof=1))
    else:
        std = 1.0
    
    if std < EPSILON:
        std = 1.0
        
    return mean, std, len(vals)

def compute_chdi_pipeline(req: CHDIComputeRequest) -> CHDIComputeResponse:
    """
    Executes the Three-Stage Composite Health Deviation Index (CHDI) sequence:
      Stage 1: Personalized Rolling Baseline & Z-Score Normalization
      Stage 2: Covariance Matrix with Tikhonov Regularization & Mahalanobis Distance
      Stage 3: Leave-One-Covariate-Out (LOCO) Permutation Attribution & Confidence Gating
    """
    history = req.historical_observations
    current = req.current_observation
    
    # Identify available active signals in current observation
    active_signals = [s for s in SIGNAL_NAMES if getattr(current, s, None) is not None]
    
    # Fallback to defaults if no signals provided
    if not active_signals:
        active_signals = ["weight", "feed", "activity"]
        
    num_points = len(history)
    
    # ── Abstention Gate: Insufficient history ──
    if num_points < req.min_history_days:
        return CHDIComputeResponse(
            cattle_id=req.cattle_id,
            score=None,
            confidence=round(min(1.0, num_points / float(N_SATURATION)), 3),
            status="abstain",
            triage_band="Abstain (Insufficient Baseline Depth < 7 Days)",
            raw_distance=0.0,
            deviations={},
            top_factors=[],
            farmer_text=f"Enrollment phase: {num_points}/{req.min_history_days} days logged. Health scoring safely withheld.",
            vet_text=f"Data-sufficiency gate active: Subject has {num_points} observations (< {req.min_history_days} required)."
        )

    # ── Stage 1: Evaluate normalized z-scores (Eq. 1, 2, 3) ──
    z_scores = {}
    means = {}
    stds = {}
    current_vec = []
    
    for s in active_signals:
        mean, std, count = compute_stage1_baseline(history, s, DEFAULT_WINDOW_SIZE)
        val = getattr(current, s)
        z = (val - mean) / (std + EPSILON)
        
        # Invert polarity for indicators where a drop is pathological
        # (e.g. drop in milk, rumination, feed, activity, weight is negative health)
        if s in ["milk", "rumination", "feed", "activity", "weight"]:
            z_score_deviation = -z if z < 0 else 0.0 # acute drops penalize health
        elif s == "temperature":
            # Pyrexia (fever) is pathological if high
            z_score_deviation = z if z > 0 else 0.0
        else:
            z_score_deviation = abs(z)
            
        z_scores[s] = float(z)
        means[s] = mean
        stds[s] = std
        current_vec.append(z)

    z_vector = np.array(current_vec, dtype=float)
    dim = len(active_signals)

    # ── Stage 2: Historical empirical covariance matrix Σ with Tikhonov regularization (Eq. 4 & 5) ──
    # Construct historical z-matrix
    historical_matrix = []
    for h in history:
        row = []
        valid_row = True
        for s in active_signals:
            h_val = getattr(h, s, None)
            if h_val is None:
                valid_row = False
                break
            h_z = (h_val - means[s]) / (stds[s] + EPSILON)
            row.append(h_z)
        if valid_row:
            historical_matrix.append(row)

    if len(historical_matrix) >= dim + 1:
        H = np.array(historical_matrix, dtype=float)
        cov = np.cov(H, rowvar=False)
        if dim == 1:
            cov = np.array([[float(cov)]])
    else:
        cov = np.eye(dim, dtype=float)

    # Apply Tikhonov regularization: Sigma_reg = Sigma + lambda * I (Eq. 5)
    cov_reg = cov + TIKHONOV_LAMBDA * np.eye(dim, dtype=float)
    
    try:
        inv_cov = np.linalg.inv(cov_reg)
    except np.linalg.LinAlgError:
        inv_cov = np.eye(dim, dtype=float)

    # Mahalanobis Distance: D_M = sqrt( z^T * Sigma_reg^-1 * z )
    origin = np.zeros(dim, dtype=float)
    try:
        raw_distance = float(mahalanobis(z_vector, origin, inv_cov))
    except Exception:
        raw_distance = float(np.linalg.norm(z_vector))

    if np.isnan(raw_distance) or np.isinf(raw_distance):
        raw_distance = float(np.linalg.norm(z_vector))

    # ── Score Normalization: 0 to 100 scale (Eq. 6) ──
    # CHDI = max(0, min(100, round(100 * (1 - D_M / D_max))))
    normalized_score = max(0.0, min(100.0, round(100.0 * (1.0 - (raw_distance / D_MAX)), 1)))

    # ── Analytical Confidence Metric (Eq. 9) ──
    # C_t = min(1, N / N_sat) * (1 - D_M / (3 * D_max))
    data_completeness = min(1.0, num_points / float(N_SATURATION))
    distance_confidence = max(0.0, 1.0 - (raw_distance / (3.0 * D_MAX)))
    confidence = round(float(data_completeness * distance_confidence), 3)

    # Gating check
    if confidence < req.min_confidence:
        status = "abstain"
        triage_band = "Abstain (Low Confidence Metric < 0.40)"
        score_val = None
    elif normalized_score < req.at_risk_below:
        status = "at-risk"
        triage_band = "At-Risk (Critical Triage Bound < 50)"
        score_val = normalized_score
    elif normalized_score < req.watch_below:
        status = "watch"
        triage_band = "Watch (Advisory Clinical Bound 50–74)"
        score_val = normalized_score
    else:
        status = "healthy"
        triage_band = "Healthy Baseline (CHDI >= 75)"
        score_val = normalized_score

    # ── Stage 3: Leave-One-Covariate-Out (LOCO) Permutation Feature Attribution (Eq. 8) ──
    attributions: List[FactorAttribution] = []
    delta_distances = []
    
    for i, s in enumerate(active_signals):
        # Permute by zeroing out the i-th feature departure
        z_permuted = np.copy(z_vector)
        z_permuted[i] = 0.0
        try:
            d_permuted = float(mahalanobis(z_permuted, origin, inv_cov))
        except Exception:
            d_permuted = float(np.linalg.norm(z_permuted))
        
        delta_d = max(0.0, raw_distance - d_permuted)
        delta_distances.append((s, delta_d, z_vector[i]))

    total_delta = sum(d[1] for d in delta_distances)
    if total_delta < 1e-6:
        # Uniform attribution if distance is minimal
        for s, _, z_val in delta_distances:
            attributions.append(FactorAttribution(
                factor=s,
                label=HUMAN_LABELS.get(s, s.title()),
                contribution_percentage=round(100.0 / dim, 1),
                direction="down" if z_val < 0 else "up",
                z_score=round(z_val, 2),
                farmer_summary=f"{HUMAN_LABELS.get(s, s.title())} within normal baseline variance.",
                vet_summary=f"{s}: z = {z_val:+.2f}σ, baseline μ = {means[s]:.1f}, σ = {stds[s]:.1f}"
            ))
    else:
        # Rank by contribution percentage
        delta_distances.sort(key=lambda x: x[1], reverse=True)
        for s, d_val, z_val in delta_distances:
            pct = round((d_val / total_delta) * 100.0, 1)
            dir_str = "down" if z_val < 0 else "up"
            
            # Formulate actionable explanations
            if s == "milk":
                f_text = f"Daily milk yield dropped by {abs(z_val * stds[s]):.1f} L ({pct}% impact on health score)."
            elif s == "rumination":
                f_text = f"Rumination time decreased significantly ({pct}% contribution). Check for early mastitis/acidosis."
            elif s == "temperature":
                f_text = f"Core body temperature elevated ({means[s] + z_val * stds[s]:.1f}°C, pyrexia indicator)."
            elif s == "feed":
                f_text = f"Feed intake appetite reduced by {abs(z_val * stds[s]):.1f} kg."
            else:
                f_text = f"{HUMAN_LABELS.get(s, s.title())} deviated {z_val:+.1f}σ from 14-day baseline."
                
            v_text = f"LOCO attribution: {pct}% | z-score: {z_val:+.2f}σ | baseline μ: {means[s]:.2f}, σ: {stds[s]:.2f}"
            
            attributions.append(FactorAttribution(
                factor=s,
                label=HUMAN_LABELS.get(s, s.title()),
                contribution_percentage=pct,
                direction=dir_str,
                z_score=round(z_val, 2),
                farmer_summary=f_text,
                vet_summary=v_text
            ))

    # Top plain summaries
    if status == "healthy":
        farmer_text = "All multi-signal health indicators are stable and aligned with the animal's personalized baseline."
    elif status == "abstain":
        farmer_text = "Establishing historical baseline profile. No abnormal deviations flagged."
    else:
        top_f = attributions[0] if attributions else None
        farmer_text = f"Advisory alert: {top_f.farmer_summary}" if top_f else "Physiological deviation detected."

    vet_text = f"CHDI: {score_val if score_val is not None else 'Abstain'} (D_M={raw_distance:.2f}, C_t={confidence:.2f}) | Primary driver: {attributions[0].factor if attributions else 'none'}"

    return CHDIComputeResponse(
        cattle_id=req.cattle_id,
        score=score_val,
        confidence=confidence,
        status=status,
        triage_band=triage_band,
        raw_distance=round(raw_distance, 3),
        deviations={s: round(z_scores[s], 2) for s in active_signals},
        top_factors=attributions,
        farmer_text=farmer_text,
        vet_text=vet_text
    )
