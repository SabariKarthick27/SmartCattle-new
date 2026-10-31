import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_system_design_diagram():
    os.makedirs('generated_figures', exist_ok=True)
    
    # Create canvas with optimal dimensions
    fig, ax = plt.subplots(figsize=(16, 11), dpi=300)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 11)
    ax.axis('off')
    
    # Background fill
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    
    # Title Header Banner
    title_box = patches.FancyBboxPatch((0.6, 10.1), 14.8, 0.7, boxstyle="round,pad=0.08", 
                                       facecolor='#0F3D32', edgecolor='#047857', linewidth=1.5)
    ax.add_patch(title_box)
    ax.text(8.0, 10.45, "SmartCattle: Real-Time Precision Livestock System Design Architecture", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='white', fontfamily='sans-serif')
    
    # Helper to draw rounded module boxes
    def draw_box(x, y, w, h, title, subtitle, items, bg_color, border_color, indent_left=0.25):
        # Outer card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", 
                                      facecolor=bg_color, edgecolor=border_color, linewidth=1.5)
        ax.add_patch(card)
        # Header banner
        header = patches.FancyBboxPatch((x, y + h - 0.52), w, 0.52, boxstyle="round,pad=0.04",
                                        facecolor=border_color, edgecolor=border_color)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.26, title, ha='center', va='center', 
                fontsize=10.5, fontweight='bold', color='white', fontfamily='sans-serif')
        
        if subtitle:
            ax.text(x + w/2, y + h - 0.72, subtitle, ha='center', va='center', 
                    fontsize=8.5, fontstyle='italic', color='#475569', fontfamily='sans-serif')
            start_y = y + h - 1.02
        else:
            start_y = y + h - 0.80
            
        for i, itm in enumerate(items):
            ax.text(x + indent_left, start_y - (i * 0.32), f"• {itm}", ha='left', va='center', 
                    fontsize=8.2, color='#1E293B', fontfamily='sans-serif')

    # Helper for connector arrows
    def draw_arrow(x1, y1, x2, y2, label="", color='#0284C7', style='<->', rad=0.0, label_pos=0.5, label_offset=(0, 0)):
        connection = f"arc3,rad={rad}" if rad != 0.0 else "arc3,rad=0"
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle=style, color=color, lw=1.8, 
                                    connectionstyle=connection, shrinkA=4, shrinkB=4))
        if label:
            mx = x1 + (x2 - x1) * label_pos + label_offset[0]
            my = y1 + (y2 - y1) * label_pos + label_offset[1]
            ax.text(mx, my, label, ha='center', va='center', fontsize=7.6,
                    fontweight='bold', color=color, 
                    bbox=dict(boxstyle='round,pad=0.20', facecolor='white', edgecolor=color, linewidth=1.1, alpha=0.95))

    # -------------------------------------------------------------
    # TIER 1: CLIENT LAYER (Top)
    # -------------------------------------------------------------
    draw_box(0.6, 7.8, 4.6, 2.0, "1. Farmer Mobile PWA", "Edge Client Interface",
             ["Camera QR Ear-Tag Optical Scanner", "Daily Manual Logs (Milk, Feed, Weight)", "Real-Time Herd Health Dashboard", "Instant Vet Escalation Request"],
             '#EFF6FF', '#2563EB')

    draw_box(5.7, 7.8, 4.6, 2.0, "2. Veterinarian Clinical Portal", "Decision & Feedback Hub",
             ["Urgent Triage Queue (CRITICAL / HIGH)", "Clinical Diagnosis & Vitals Record (°C)", "Dual-Tier LOCO Factor Explanations", "AI Ground-Truth Outcome Feedback"],
             '#ECFDF5', '#059669')

    draw_box(10.8, 7.8, 4.6, 2.0, "3. Admin & Surveillance Console", "Central Operations",
             ["Farmer & Vet Verification Gatekeeper", "Multi-Farm Spatio-Temporal Map", "Epidemiological Outbreak Clustering", "System Metric & Model Configuration"],
             '#FEF3C7', '#D97706')

    # -------------------------------------------------------------
    # TIER 2: API GATEWAY & APPLICATION SERVER (Middle)
    # -------------------------------------------------------------
    draw_box(2.8, 5.0, 10.4, 2.05, "API Gateway & Application Server (Next.js 16 App Router)", "Security & Orchestration Engine",
             ["NextAuth.js Session Guards & Role-Based Access Control (RBAC: Farmer / Vet / Admin)",
              "RESTful Endpoints (/api/cattle, /api/scan/[token], /api/vet/cases, /api/weekly-analysis)",
              "Signal Imputation & Deviation Vector Normalization (Δx = [Weight, Feed, Milk, Vitals])",
              "Asynchronous Event Notification Dispatcher & SMS Gateway"],
             '#F1F5F9', '#334155')

    # -------------------------------------------------------------
    # TIER 3: MACHINE LEARNING MICROSERVICE (Bottom Left)
    # -------------------------------------------------------------
    draw_box(0.5, 0.9, 7.0, 3.4, "AI / ML Microservice (Python FastAPI)", "High-Performance Analytics Core",
             ["Personalized Historical Baseline Matrix Generator (μ, Σ)",
              "Regularized Mahalanobis Distance Engine: D_M(x) = √((x-μ)ᵀ Σ_reg⁻¹ (x-μ))",
              "Matrix Condition Number Stability Check: κ(Σ) = λ_max / λ_min < 100",
              "Confidence-Aware Abstention Gate: Rejects if C < 0.40 or N < 7 pts",
              "Leave-One-Covariate-Out (LOCO) Root-Cause Feature Attribution",
              "Veterinarian-in-the-Loop Active Learning Re-Classifier"],
             '#FAF5FF', '#7C3AED')

    # -------------------------------------------------------------
    # TIER 4: PERSISTENCE & DATA TIER (Bottom Right)
    # -------------------------------------------------------------
    draw_box(8.5, 0.9, 7.0, 3.4, "Database & Storage Layer (PostgreSQL + Prisma ORM)", "Structured Persistent Store",
             ["Cattle Registry: Tag IDs, Breed, Age, Birthdate, Farm Association",
              "Time-Series Vitals: WeightLog, FeedLog, MilkLog, TempLog, RumLog",
              "CHDI History: Daily 0-100 Scores, Status Flags, LOCO Risk JSON",
              "Clinical Records: VetCases, Diagnosis, Prescriptions, AI Outcomes",
              "Geo-Spatial Data: GPS Coordinates, Regional District Aggregations"],
             '#F0FDF4', '#16A34A')

    # Connectors - Top to Middle
    draw_arrow(2.9, 7.8, 4.5, 7.05, "HTTPS / QR Token", color='#2563EB', style='->', label_offset=(-0.35, 0.0))
    draw_arrow(8.0, 7.8, 8.0, 7.05, "Diagnosis & Feedback", color='#059669', style='->', label_offset=(0.0, 0.0))
    draw_arrow(13.1, 7.8, 11.5, 7.05, "Surveillance Queries", color='#D97706', style='->', label_offset=(0.35, 0.0))

    # Connectors - Middle to Bottom
    draw_arrow(4.8, 5.0, 4.0, 4.3, "REST (Deviation Vector ⇄ CHDI & LOCO)", color='#7C3AED', style='<->', label_pos=0.5, label_offset=(0.0, 0.0))
    draw_arrow(11.2, 5.0, 12.0, 4.3, "Prisma ORM (Mutations ⇄ Time-Series Records)", color='#16A34A', style='<->', label_pos=0.5, label_offset=(0.0, 0.0))

    # ML to Database Direct Cross-link (Centered in the gap)
    draw_arrow(7.5, 2.9, 8.5, 2.9, "90-Day Baseline Logs", color='#0284C7', style='<-', label_offset=(0.0, 0.22))
    draw_arrow(8.5, 1.7, 7.5, 1.7, "Ground-Truth Labels", color='#EA580C', style='->', label_offset=(0.0, -0.22))

    # Footer note
    ax.text(8.0, 0.35, "Real-Time Pipeline: Latency < 150ms | Sensor-Optional Resilience | Clinical Explainability | Active Learning Feedback Loop",
            ha='center', va='center', fontsize=9.0, fontweight='bold', color='#475569', fontfamily='sans-serif')

    out_path = 'generated_figures/smartcattle_system_design_architecture.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Generated successfully: {out_path}")
    return out_path

if __name__ == "__main__":
    create_system_design_diagram()
