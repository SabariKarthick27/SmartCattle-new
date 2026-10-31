import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os
import shutil

def set_run_font(run, font_name="Times New Roman", size_pt=11, bold=False, italic=False, subscript=False, superscript=False, color_rgb=(0,0,0)):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    run.font.subscript = subscript
    run.font.superscript = superscript
    run.font.color.rgb = RGBColor(*color_rgb)
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:ascii'), font_name)
    rFonts.set(qn('w:hAnsi'), font_name)
    rFonts.set(qn('w:cs'), font_name)

def build_perfect_math_document():
    # Read from SmartCattle_Project_Report_Aligned_MASTER.docx (which has user edits)
    src_file = "SmartCattle_Project_Report_Aligned_MASTER.docx"
    doc = docx.Document(src_file)
    print(f"Loaded {src_file}: {len(doc.paragraphs)} paragraphs, {len(doc.tables)} tables.")

    # 1. Clean Table 10 (Severity Bands) and Table 11 (Telemetry Features)
    if len(doc.tables) > 10:
        t10 = doc.tables[10]
        for row in t10.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.text = (p.text
                        .replace("$D_M$", "DM")
                        .replace("$D_M < 0.70$", "DM < 0.70")
                        .replace("$0.70 \\le D_M < 1.45$", "0.70 ≤ DM < 1.45")
                        .replace("$1.45 \\le D_M < 2.65$", "1.45 ≤ DM < 2.65")
                        .replace("$D_M \\ge 2.65$", "DM ≥ 2.65")
                        .replace("$", ""))
                    for r in p.runs:
                        set_run_font(r, font_name="Times New Roman", size_pt=12)

    if len(doc.tables) > 11:
        t11 = doc.tables[11]
        for row in t11.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.text = (p.text
                        .replace("($x_k$)", "(xk)")
                        .replace("($x_1$)", "(x₁)")
                        .replace("($x_2$)", "(x₂)")
                        .replace("($x_3$)", "(x₃)")
                        .replace("($x_4$)", "(x₄)")
                        .replace("($x_5$)", "(x₅)")
                        .replace("$", ""))
                    for r in p.runs:
                        set_run_font(r, font_name="Times New Roman", size_pt=12)

    # 2. Fix inline body paragraphs
    for p in doc.paragraphs:
        t = p.text
        if "($x_1$)" in t or "$x_1$" in t:
            p.text = (t
                .replace("($x_1$)", "(x₁)")
                .replace("($x_2$)", "(x₂)")
                .replace("($x_3$)", "(x₃)")
                .replace("($x_4$)", "(x₄)")
                .replace("($x_5$)", "(x₅)")
                .replace("$x_1$", "x₁")
                .replace("$x_2$", "x₂")
                .replace("$x_3$", "x₃")
                .replace("$x_4$", "x₄")
                .replace("$x_5$", "x₅"))
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        if "$D_M$" in t and "\\frac" not in t:
            p.text = p.text.replace("$D_M$", "DM (Mahalanobis distance)")
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        if "$S < -2.0$" in t:
            p.text = p.text.replace("$k=7$", "k = 7").replace("($S < -2.0$)", "(slope S < −2.0)")
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        if "$N \\ge 7$" in t or "$N_min" in t or "$N_{min}" in t:
            p.text = p.text.replace("$N \\ge 7$", "N ≥ 7 days").replace("$N_{min}=7$", "N_min = 7 days").replace("$N_{min} = 7$", "N_min = 7 days")
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        if "$|W| = 14$" in t:
            p.text = p.text.replace("$|W| = 14$", "|W| = 14 days").replace("$\\lambda_{reg} = 10^{-3}$", "λ_reg = 10⁻³").replace("$\\Sigma$", "Σ")
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        if "\\frac{TP}{TP + FN}" in t:
            p.text = (
                "System evaluation follows standard statistical metrics:\n"
                "• Sensitivity (Recall): Sensitivity = TP / (TP + FN), measuring the proportion of true clinical anomalies detected.\n"
                "• Specificity: Specificity = TN / (TN + FP), measuring resistance against false alarms on healthy baseline days.\n"
                "• Precision: Precision = TP / (TP + FP), measuring the proportion of generated alerts corresponding to genuine clinical distress.\n"
                "• F1-Score: F1-Score = 2 × (Precision × Recall) / (Precision + Recall), the harmonic mean of precision and recall.\n"
                "• Diagnostic Lead Time: Advance warning lead time (2.4 days on average) between initial sub-clinical CHDI deviation and observable clinical symptoms."
            )
            for r in p.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

    # Helper to add equation block with rich subscript/superscript "Where:" explanations
    def insert_equation_block_before(target_para, img_path, eq_num_str, title_str, bullets_data):
        # 1. Equation image
        p_img = target_para.insert_paragraph_before()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        r_img = p_img.add_run()
        r_img.add_picture(img_path, width=Inches(4.8))

        # 2. Equation caption
        p_cap = target_para.insert_paragraph_before()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(3)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(f"Equation ({eq_num_str}): {title_str}")
        set_run_font(r_cap, font_name="Times New Roman", size_pt=11.5, bold=True)

        # 3. Where: header (LEFT ALIGNED)
        p_w_head = target_para.insert_paragraph_before()
        p_w_head.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_w_head.paragraph_format.space_before = Pt(3)
        p_w_head.paragraph_format.space_after = Pt(2)
        p_w_head.paragraph_format.keep_with_next = True
        r_wh = p_w_head.add_run("Where:")
        set_run_font(r_wh, font_name="Times New Roman", size_pt=11, bold=True, italic=True)

        # 4. Each bullet item (LEFT ALIGNED to avoid awkward spacing gaps!)
        for run_specs, plain_text in bullets_data:
            p_b = target_para.insert_paragraph_before()
            p_b.alignment = WD_ALIGN_PARAGRAPH.LEFT  # NEVER JUSTIFY SHORT BULLET LINES!
            p_b.paragraph_format.space_before = Pt(1)
            p_b.paragraph_format.space_after = Pt(3)
            p_b.paragraph_format.line_spacing = 1.15
            p_b.paragraph_format.left_indent = Inches(0.25)
            
            # Bullet symbol
            r_bullet = p_b.add_run("• ")
            set_run_font(r_bullet, font_name="Times New Roman", size_pt=11, bold=True)
            
            # Formatted math symbol runs
            for txt, is_it, is_sub, is_sup in run_specs:
                r_sym = p_b.add_run(txt)
                set_run_font(r_sym, font_name="Times New Roman", size_pt=11, italic=is_it, subscript=is_sub, superscript=is_sup)
                
            # Definition explanation text
            r_exp = p_b.add_run(plain_text)
            set_run_font(r_exp, font_name="Times New Roman", size_pt=11)

    def insert_text_before(target_para, text):
        p = target_para.insert_paragraph_before()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        set_run_font(r, font_name="Times New Roman", size_pt=12)
        return p

    # Find Section 4.7 paragraphs
    idx_p173 = -1
    for i, p in enumerate(doc.paragraphs):
        if "The mathematical foundation of the proposed system executes across three analytical stages" in p.text:
            idx_p173 = i
            break

    if idx_p173 != -1:
        p_intro = doc.paragraphs[idx_p173]
        p_intro.text = (
            "The mathematical foundation of the proposed system executes across three analytical stages as formalized in Section IV of the IEEE paper:\n\n"
            "Stage 1: Individual Rolling Baseline & Standardized Deviations:\n"
            "Rather than comparing an animal against arbitrary population-wide static thresholds, Stage 1 establishes an individualized historical baseline over a 14-day observation window (|W| = 14). For each physiological parameter k (where k ∈ {1, 2, 3, 4, 5}), the baseline mean and sample variance are computed using Equation (4.1) and Equation (4.2)."
        )
        for r in p_intro.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        target_before_t10 = doc.paragraphs[idx_p173 + 1]

        # Equation 4.1
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_1.png",
            "4.1",
            "Rolling Baseline Mean Estimation",
            [
                ([("μ", True, False, False), ("i,k", True, True, False), ("(t)", False, False, False)],
                 " = Individualized 14-day rolling historical baseline mean for cow i across parameter k."),
                ([("|W|", False, False, False)],
                 " = Baseline observation window length (|W| = 14 consecutive daily records)."),
                ([("x", True, False, False), ("i,k", True, True, False), ("(t − m)", False, False, False)],
                 " = Historical daily measurement logged on day (t − m).")
            ]
        )

        # Equation 4.2
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_2.png",
            "4.2",
            "Rolling Baseline Sample Variance",
            [
                ([("σ", True, False, False), ("i,k", True, True, False), ("²(t)", False, False, False)],
                 " = Unbiased sample variance capturing animal i's natural biological variation."),
                ([("(|W| − 1)", False, False, False)],
                 " = Bessel's sample variance correction factor (degrees of freedom df = 13)."),
                ([("(x", True, False, False), ("i,k", True, True, False), ("(t − m) − μ", False, False, False), ("i,k", True, True, False), ("(t))²", False, False, False)],
                 " = Squared deviation of daily measurement from the rolling baseline mean.")
            ]
        )

        # Lead-in for Z-score
        insert_text_before(target_before_t10,
            "When a new daily measurement is recorded, the raw value is normalized into a dimensionless standardized Z-score deviation using Equation (4.3). A regularization constant ε = 10⁻⁴ is included in the denominator to ensure numerical stability and prevent division-by-zero."
        )

        # Equation 4.3
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_3.png",
            "4.3",
            "Standardized Individual Deviation (Z-Score)",
            [
                ([("z", True, False, False), ("i,k", True, True, False), ("(t)", False, False, False)],
                 " = Dimensionless standardized Z-score deviation from personal baseline."),
                ([("x", True, False, False), ("i,k", True, True, False), ("(t)", False, False, False)],
                 " = Newly observed measurement (e.g., daily milk yield, feed intake, rumination)."),
                ([("ε", True, False, False)],
                 " = 10⁻⁴ = Numerical stabilization constant preventing zero-variance division.")
            ]
        )

        # Stage 2 Lead-in
        insert_text_before(target_before_t10,
            "Stage 2: Multivariate Covariance & Mahalanobis CHDI Formulation:\n"
            "Because bovine disorders affect multiple physiological systems simultaneously (e.g., subclinical mastitis causes concurrent drops in milk and feed intake alongside elevated core body temperature), Stage 2 models cross-variable dependencies using the regularized empirical covariance matrix Σ in Equation (4.4)."
        )

        # Equation 4.4
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_4.png",
            "4.4",
            "Regularized Empirical Covariance Matrix",
            [
                ([("Σ(t)", True, False, False)],
                 " = 5 × 5 empirical covariance matrix capturing dependencies across all 5 telemetry features."),
                ([("z", True, False, False), ("i", True, True, False), ("(t − m)", False, False, False)],
                 " = 5-dimensional standardized deviation vector at observation step (t − m)."),
                ([("λ", True, False, False), ("reg", True, True, False), (" · I", False, False, False)],
                 " = Tikhonov ridge shrinkage regularization (λ_reg = 10⁻³), guaranteeing positive-definite matrix inversion.")
            ]
        )

        # Mahalanobis Lead-in
        insert_text_before(target_before_t10,
            "The multi-signal anomaly distance is calculated in covariance-weighted space using the multivariate Mahalanobis distance in Equation (4.5). This distance quantifies the multi-dimensional departure of current vitals from the animal's personal physiological centroid."
        )

        # Equation 4.5
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_5.png",
            "4.5",
            "Multivariate Mahalanobis Anomaly Distance",
            [
                ([("D", True, False, False), ("M", True, True, False), ("(z", False, False, False), ("i", True, True, False), (")", False, False, False)],
                 " = Multivariate Mahalanobis anomaly distance in covariance-weighted space."),
                ([("z", True, False, False), ("i", True, True, False)],
                 " = Normalized 5-dimensional deviation vector: [z_weight, z_feed, z_milk, z_temp, z_activity]ᵀ."),
                ([("Σ⁻¹", False, False, False)],
                 " = Inverted regularized covariance matrix weighting correlated signals.")
            ]
        )

        # CHDI Mapping Lead-in
        insert_text_before(target_before_t10,
            "To provide an intuitive metric for farmers and clinicians, the raw Mahalanobis distance D_M is mapped to a bounded Composite Health Deviation Index (CHDI) on a 0 to 100 scale using the exponential decay formulation in Equation (4.6)."
        )

        # Equation 4.6
        insert_equation_block_before(
            target_before_t10,
            "patent_figures/equations/eq_6.png",
            "4.6",
            "Bounded Composite Health Deviation Index (CHDI)",
            [
                ([("CHDI(z", False, False, False), ("i", True, True, False), (")", False, False, False)],
                 " = Continuous health score bounded between 100 (Optimal Health) and 0 (Severe Critical Distress)."),
                ([("λ", True, False, False)],
                 " = 0.35 = Calibrated exponential decay scaling factor."),
                ([("Clinical Bands", True, False, False)],
                 ": Healthy (80–100), Watch (60–79), Warning (40–59), and Critical (0–39).")
            ]
        )

    # Now handle Stage 3
    idx_p175_new = -1
    for i, p in enumerate(doc.paragraphs):
        if "Stage 3: Temporal Trend, Explainability, and Uncertainty Estimation:" in p.text:
            idx_p175_new = i
            break

    if idx_p175_new != -1:
        p_st3 = doc.paragraphs[idx_p175_new]
        p_st3.text = (
            "Stage 3: Temporal Trend, Explainability, and Uncertainty Estimation:\n"
            "Stage 3 enhances clinical utility through three algorithmic decision mechanisms: evaluating 7-day temporal trends, attributing feature contributions, and enforcing uncertainty gating."
        )
        for r in p_st3.runs: set_run_font(r, font_name="Times New Roman", size_pt=12)

        target_st3 = doc.paragraphs[idx_p175_new + 1]

        # Equation 4.7
        insert_equation_block_before(
            target_st3,
            "patent_figures/equations/eq_7.png",
            "4.7",
            "7-Day Temporal Trend Slope (OLS Regression)",
            [
                ([("S", True, False, False)],
                 " = 7-day health trajectory slope evaluated across the last k = 7 consecutive CHDI scores."),
                ([("t", True, False, False)],
                 " = Time step index (t ∈ {1, 2, ..., 7}) with midpoint t̄ = 4."),
                ([("Clinical Rule", True, False, False)],
                 ": Negative slope (S < −2.0) indicates rapid health deterioration, escalating alert priority before static bounds are breached.")
            ]
        )

        # Equation 4.8
        insert_equation_block_before(
            target_st3,
            "patent_figures/equations/eq_8.png",
            "4.8",
            "Permutation Feature Importance Attribution",
            [
                ([("C", True, False, False), ("k", True, True, False)],
                 " = Percentage diagnostic contribution (%) of parameter k to the total anomaly alert."),
                ([("D", True, False, False), ("M", True, True, False), ("(z)", False, False, False)],
                 " = Full Mahalanobis anomaly distance across all 5 telemetry features."),
                ([("D", True, False, False), ("M", True, True, False), ("(z", False, False, False), ("−k", True, True, False), (")", False, False, False)],
                 " = Counterfactual distance evaluated with variable k held at baseline.")
            ]
        )

        # Equation 4.9
        insert_equation_block_before(
            target_st3,
            "patent_figures/equations/eq_9.png",
            "4.9",
            "Data-Sufficiency Uncertainty Gate",
            [
                ([("Conf(N)", False, False, False)],
                 " = Uncertainty confidence coefficient scaling between 0.0 and 1.0."),
                ([("N", True, False, False)],
                 " = Count of consecutive valid daily observation logs recorded for the cow."),
                ([("N", True, False, False), ("min", True, True, False)],
                 " = 7 days = Minimum logging threshold required before issuing definitive clinical alerts, preventing false alarms on newly registered cows.")
            ]
        )

    # Output file
    out_file = "SmartCattle_Project_Report_PERFECT_MATH.docx"
    doc.save(out_file)
    print(f"Successfully generated {out_file} with perfect readable subscripts and formatting!")

    # Try copying to other files if unlocked
    for f in ["SmartCattle_Project_Report.docx", "SmartCattle_Project_Report_Aligned_MASTER.docx", "SmartCattle_Project_Report_Aligned.docx"]:
        try:
            shutil.copy2(out_file, f)
            print(f"Copied to {f}")
        except PermissionError:
            print(f"{f} currently locked by Word.")

if __name__ == "__main__":
    build_perfect_math_document()
