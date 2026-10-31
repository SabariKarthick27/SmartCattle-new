import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
import os

def create_modules_diagram(output_path="smartcattle_system_modules_diagram.png", dark_mode=False):
    # Set high DPI and wide presentation canvas
    fig_w, fig_h = 16.5, 11.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)
    
    bg_color = "#ffffff" if not dark_mode else "#0b0f19"
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # 7 Modules definitions arranged in natural serpentine pipeline (1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 3)
    cards = [
        # Row 1 (Left to Right: 1 -> 2 -> 3)
        {
            "id": 1,
            "title": "Cattle Database & Profile Registry:",
            "desc": "Stores pre-registered cattle biographical details including 128-bit UUID tags, breed taxonomy, parity, age, and historical vaccination records. The database serves as the authoritative reference for all real-time field authentication and longitudinal tracking.",
            "row": 0, "col": 0
        },
        {
            "id": 2,
            "title": "QR Identity & Edge Acquisition Layer:",
            "desc": "Weather-proof TPU ear tags etched with cryptographic QR matrices securely link physical cattle to cloud profiles. Standard smartphone cameras capture daily milk yield, feed intake, and activity vitals directly in the field without requiring costly RFID hardware.",
            "row": 0, "col": 1
        },
        {
            "id": 3,
            "title": "Three-Stage CHDI Analytics Engine:",
            "desc": "Computes dynamic moving-average physiological baselines and evaluates multi-signal anomaly departures via covariance-weighted Mahalanobis distance with Tikhonov regularization, generating personalized 0–100 CHDI scores.",
            "row": 0, "col": 2
        },
        # Row 2 (Right to Left: 4 -> 5 -> 6)
        {
            "id": 4,
            "title": "Temporal Trajectory & Trend Engine:",
            "desc": "Performs rolling 7-day least-squares linear trend regression across CHDI values. Quantifies health degradation slope to detect subclinical mastitis, lameness, and metabolic disorders up to four days prior to acute clinical symptom manifestation.",
            "row": 1, "col": 2
        },
        {
            "id": 5,
            "title": "Explainability & Attribution Module:",
            "desc": "Decomposes multivariate anomaly departures via Leave-One-Covariate-Out (LOCO) permutation analysis. Translates raw mathematical z-scores into intuitive farmer advisories and granular clinical triage contribution charts for attending veterinarians.",
            "row": 1, "col": 1
        },
        {
            "id": 6,
            "title": "Role-Based Web Portal & Dashboard:",
            "desc": "A responsive Next.js web application offering dedicated views for Farmers, Veterinarians, and Cooperative Admins. Displays live herd health heatmaps, prioritized triage alert queues, vaccination schedules, and interactive trajectory graphs.",
            "row": 1, "col": 0
        },
        # Row 3 (Centered: 7)
        {
            "id": 7,
            "title": "Automated VetCase Dispatch & Feedback Learning:",
            "desc": "Automatically dispatches prioritized clinical tickets when health scores drop into the critical At-Risk band (CHDI < 50). Records verified on-site veterinary diagnoses to continuously retrain and refine the supervised machine learning risk models.",
            "row": 2, "col": 1
        }
    ]

    # Grid layout parameters
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    card_w = 28.0
    card_h = 24.5
    
    gap_x = 5.2
    gap_y = 6.2
    
    start_x = (100 - (3 * card_w + 2 * gap_x)) / 2  # ~2.8
    start_y = 96.0 - card_h  # top row start
    
    box_color = "#111111" if not dark_mode else "#1e293b"
    edge_color = "#111111" if not dark_mode else "#38bdf8"
    title_color = "#ffffff"
    text_color = "#f8fafc"
    
    card_positions = {}
    
    for card in cards:
        r = card["row"]
        c = card["col"]
        
        x = start_x + c * (card_w + gap_x)
        y = start_y - r * (card_h + gap_y)
        card_positions[card["id"]] = {"x": x, "y": y, "w": card_w, "h": card_h}
        
        # Draw rounded rectangle
        box = patches.FancyBboxPatch(
            (x, y), card_w, card_h,
            boxstyle="round,pad=0.0,rounding_size=2.8",
            facecolor=box_color,
            edgecolor=edge_color,
            linewidth=1.2,
            zorder=3
        )
        ax.add_patch(box)
        
        center_x = x + card_w / 2.0
        
        title_wrapped = "\n".join(textwrap.wrap(card["title"], width=26))
        desc_wrapped = "\n".join(textwrap.wrap(card["desc"], width=34))
        
        title_y = y + card_h - 2.5
        
        ax.text(
            center_x, title_y,
            title_wrapped,
            ha='center', va='top',
            color=title_color,
            fontsize=10.2,
            fontweight='bold',
            family='sans-serif',
            linespacing=1.18,
            zorder=4
        )
        
        num_title_lines = title_wrapped.count('\n') + 1
        desc_y = title_y - (num_title_lines * 2.3) - 1.1
        
        ax.text(
            center_x, desc_y,
            desc_wrapped,
            ha='center', va='top',
            color=text_color,
            fontsize=8.1,
            fontweight='normal',
            family='sans-serif',
            linespacing=1.34,
            zorder=4
        )

    # ------------------ DRAW ARROWS ------------------
    arrow_color = "#1e293b"  # Deep slate arrow
    lw = 2.4
    
    def draw_arrow(start_pt, end_pt, label="", label_pos=(0, 0), connectionstyle=None):
        if connectionstyle:
            arrow = patches.FancyArrowPatch(
                start_pt, end_pt,
                arrowstyle='-|>,head_length=8.5,head_width=5.5',
                connectionstyle=connectionstyle,
                color=arrow_color,
                linewidth=lw,
                zorder=2
            )
            ax.add_patch(arrow)
        else:
            arrow = patches.FancyArrowPatch(
                start_pt, end_pt,
                arrowstyle='-|>,head_length=8.5,head_width=5.5',
                color=arrow_color,
                linewidth=lw,
                zorder=2
            )
            ax.add_patch(arrow)
            
        if label:
            lx, ly = label_pos
            ax.text(
                lx, ly, label,
                ha='center', va='center',
                fontsize=7.3, fontweight='bold',
                color="#0f172a", family='sans-serif',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#f8fafc', edgecolor='#cbd5e1', lw=0.9),
                zorder=5
            )

    p1 = card_positions[1]
    p2 = card_positions[2]
    p3 = card_positions[3]
    p4 = card_positions[4]
    p5 = card_positions[5]
    p6 = card_positions[6]
    p7 = card_positions[7]
    
    # 1. Box 1 -> Box 2 (Top Left to Top Center)
    draw_arrow(
        (p1["x"] + p1["w"], p1["y"] + p1["h"]*0.5),
        (p2["x"], p2["y"] + p2["h"]*0.5),
        label="UUID & Tag Binding",
        label_pos=(p1["x"] + p1["w"] + gap_x/2, p1["y"] + p1["h"]*0.5)
    )
    
    # 2. Box 2 -> Box 3 (Top Center to Top Right)
    draw_arrow(
        (p2["x"] + p2["w"], p2["y"] + p2["h"]*0.5),
        (p3["x"], p3["y"] + p3["h"]*0.5),
        label="Field Telemetry Vitals",
        label_pos=(p2["x"] + p2["w"] + gap_x/2, p2["y"] + p2["h"]*0.5)
    )
    
    # 3. Box 3 -> Box 4 (Top Right down to Middle Right)
    draw_arrow(
        (p3["x"] + p3["w"]*0.5, p3["y"]),
        (p4["x"] + p4["w"]*0.5, p4["y"] + p4["h"]),
        label="CHDI Scores",
        label_pos=(p3["x"] + p3["w"]*0.5, p3["y"] - gap_y/2)
    )
    
    # 4. Box 4 -> Box 5 (Middle Right to Middle Center)
    draw_arrow(
        (p4["x"], p4["y"] + p4["h"]*0.5),
        (p5["x"] + p5["w"], p5["y"] + p5["h"]*0.5),
        label="7-Day Slope Trends",
        label_pos=(p5["x"] + p5["w"] + gap_x/2, p4["y"] + p4["h"]*0.5)
    )
    
    # 5. Box 5 -> Box 6 (Middle Center to Middle Left)
    draw_arrow(
        (p5["x"], p5["y"] + p5["h"]*0.5),
        (p6["x"] + p6["w"], p6["y"] + p6["h"]*0.5),
        label="LOCO Attributions",
        label_pos=(p6["x"] + p6["w"] + gap_x/2, p5["y"] + p5["h"]*0.5)
    )
    
    # 6. Box 6 -> Box 7 (Middle Left down to Bottom Center)
    draw_arrow(
        (p6["x"] + p6["w"]*0.5, p6["y"]),
        (p7["x"], p7["y"] + p7["h"]*0.6),
        label="Critical Triage (CHDI < 50)",
        label_pos=(p6["x"] + p6["w"]*0.5 + 4.8, p6["y"] - gap_y*0.75),
        connectionstyle="arc3,rad=0.22"
    )
    
    # 7. Box 7 -> Feedback Loop to Box 3 (Bottom Center up-right to Top Right / Box 1)
    # Let's route from Box 7's right side to Box 4's bottom or Box 3 directly:
    draw_arrow(
        (p7["x"] + p7["w"], p7["y"] + p7["h"]*0.6),
        (p4["x"] + p4["w"]*0.5, p4["y"]),
        label="Vet Ground-Truth & ML Retraining Loop",
        label_pos=(p7["x"] + p7["w"] + 5.2, p7["y"] + p7["h"]*0.75),
        connectionstyle="arc3,rad=-0.22"
    )

    # Save high-res PNG and vector SVG
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.15)
    
    svg_path = os.path.splitext(output_path)[0] + ".svg"
    plt.savefig(svg_path, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.15)
    
    plt.close()
    print(f"Generated diagram with arrows successfully at:\n  - {output_path}\n  - {svg_path}")

if __name__ == "__main__":
    create_modules_diagram("smartcattle_system_modules_diagram.png")
    create_modules_diagram("generated_figures/smartcattle_system_modules_diagram.png")
    print("All diagrams with arrows generated successfully.")
