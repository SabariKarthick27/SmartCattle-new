from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ObservationVector(BaseModel):
    milk: Optional[float] = Field(None, description="Daily milk yield in litres")
    rumination: Optional[float] = Field(None, description="Rumination duration in minutes")
    temperature: Optional[float] = Field(None, description="Core body temperature in °C")
    activity: Optional[float] = Field(None, description="Locomotion steps or activity index 0-100")
    feed: Optional[float] = Field(None, description="Feed intake quantity in kg")
    weight: Optional[float] = Field(None, description="Body weight in kg")

class SignalDeviation(BaseModel):
    milkDeviation: Optional[float] = 0.0
    ruminationDeviation: Optional[float] = 0.0
    temperatureDeviation: Optional[float] = 0.0
    activityDeviation: Optional[float] = 0.0
    feedDeviation: Optional[float] = 0.0
    weightDeviation: Optional[float] = 0.0

class HistoricalObservation(BaseModel):
    timestamp: str
    milk: Optional[float] = None
    rumination: Optional[float] = None
    temperature: Optional[float] = None
    activity: Optional[float] = None
    feed: Optional[float] = None
    weight: Optional[float] = None

class CHDIComputeRequest(BaseModel):
    cattle_id: str
    current_observation: ObservationVector
    historical_observations: List[HistoricalObservation] = []
    min_confidence: float = 0.40
    min_history_days: int = 7
    watch_below: float = 75.0
    at_risk_below: float = 50.0

class FactorAttribution(BaseModel):
    factor: str
    label: str
    contribution_percentage: float
    direction: str
    z_score: float
    farmer_summary: str
    vet_summary: str

class CHDIComputeResponse(BaseModel):
    cattle_id: str
    score: Optional[float] = None # 0-100; None when abstaining
    confidence: float
    status: str # "healthy" | "watch" | "at-risk" | "abstain"
    triage_band: str
    raw_distance: float
    deviations: Dict[str, float]
    top_factors: List[FactorAttribution] = []
    farmer_text: str
    vet_text: str

class ExplainRequest(BaseModel):
    deviations: Dict[str, float]
    covariance_matrix: List[List[float]]
    raw_distance: float

class VetFeedbackSample(BaseModel):
    score: float
    confidence: float
    deviations: Dict[str, float]
    confirmed_outcome: str # "healthy" | "acute_mastitis" | "subclinical_ketosis" | "lameness" | "false_positive"

class RetrainRequest(BaseModel):
    samples: List[VetFeedbackSample]

class RetrainResponse(BaseModel):
    status: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    sample_count: int
    classes: List[str]
