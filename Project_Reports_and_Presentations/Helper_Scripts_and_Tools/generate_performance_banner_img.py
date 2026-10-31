import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image

os.makedirs('generated_figures', exist_ok=True)

# -------------------------------------------------------------
# 1. STANDALONE PERFORMANCE BANNER IMAGE
# -------------------------------------------------------------
def generate_metrics_banner():
    # Width: 10 inches, Height: 2.2 inches, 300 DPI
    fig, ax = plt.subplots(figsize=(10.0, 2.3), dpi=300)
    ax.set_facecolor('#ffffff')
    fig.patch.set_facecolor('#ffffff')
    ax.axis('off')
    
    teal_color = '#156570' # Exact teal from user slide
    subtext_color = '#475569'
    note_color = '#64748b'
    
    # Title
    ax.text(0.02, 0.88, 'PROPOSED MAHALANOBIS CHDI — REPORTED PERFORMANCE',
            fontsize=12, fontweight='bold', color=teal_color,
            family='sans-serif', va='top', ha='left')
    
    metrics = [
        ("91.20%", "Sensitivity"),
        ("96.85%", "Specificity"),
        ("88.50%", "Precision"),
        ("89.82%", "F1-score"),
        ("2.4 days", "Reported lead time")
    ]
    
    x_positions = [0.10, 0.30, 0.50, 0.70, 0.90]
    
    for (num, label), x in zip(metrics, x_positions):
        # Big number
        ax.text(x, 0.52, num, fontsize=20, fontweight='bold', color=teal_color,
                family='sans-serif', va='center', ha='center')
        # Subtext label
        ax.text(x, 0.28, label, fontsize=10.5, fontweight='medium', color=subtext_color,
                family='sans-serif', va='center', ha='center')
        
    # Bottom footnote
    footnote = "Empirical evaluation across 674 longitudinal observation days and 32 verified veterinary field diagnoses in Salem district."
    ax.text(0.50, 0.06, footnote, fontsize=8.5, fontstyle='italic', color=note_color,
            family='sans-serif', va='bottom', ha='center')
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    out_path = 'generated_figures/proposed_mahalanobis_chdi_performance_banner.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    plt.close(fig)
    print(f"Generated {out_path} successfully!")
    return out_path

# -------------------------------------------------------------
# 2. FULL COMPOSITE SLIDE CONTENT (Graphs + Banner)
# -------------------------------------------------------------
def generate_full_slide_content():
    # Load the two corrected graphs
    fig4_path = 'generated_figures/fig4_longitudinal_trajectory.png'
    fig5_path = 'generated_figures/fig5_feature_importance.png'
    
    img_left = Image.open(fig4_path)
    img_right = Image.open(fig5_path)
    
    # Create combined figure: 12.0 inches wide by 6.0 inches tall
    fig = plt.figure(figsize=(12.0, 6.2), dpi=300)
    fig.patch.set_facecolor('#ffffff')
    
    # 2 top subplots for graphs
    ax1 = fig.add_axes([0.03, 0.38, 0.46, 0.58]) # Left graph
    ax2 = fig.add_axes([0.53, 0.38, 0.44, 0.58]) # Right graph
    
    ax1.imshow(img_left)
    ax1.axis('off')
    
    ax2.imshow(img_right)
    ax2.axis('off')
    
    # Bottom axis for performance banner
    ax_bottom = fig.add_axes([0.03, 0.02, 0.94, 0.32])
    ax_bottom.set_facecolor('#ffffff')
    ax_bottom.axis('off')
    
    teal_color = '#156570'
    subtext_color = '#475569'
    note_color = '#64748b'
    
    # Title
    ax_bottom.text(0.01, 0.88, 'PROPOSED MAHALANOBIS CHDI — REPORTED PERFORMANCE',
                   fontsize=13, fontweight='bold', color=teal_color,
                   family='sans-serif', va='top', ha='left')
    
    metrics = [
        ("91.20%", "Sensitivity"),
        ("96.85%", "Specificity"),
        ("88.50%", "Precision"),
        ("89.82%", "F1-score"),
        ("2.4 days", "Reported lead time")
    ]
    
    x_positions = [0.09, 0.29, 0.49, 0.69, 0.89]
    
    for (num, label), x in zip(metrics, x_positions):
        ax_bottom.text(x, 0.50, num, fontsize=21, fontweight='bold', color=teal_color,
                       family='sans-serif', va='center', ha='center')
        ax_bottom.text(x, 0.22, label, fontsize=11, fontweight='medium', color=subtext_color,
                       family='sans-serif', va='center', ha='center')
        
    footnote = "Compared with global static thresholds and univariate Z-score baselines; calibrated with 32 verified veterinary field diagnoses in Salem district."
    ax_bottom.text(0.50, 0.02, footnote, fontsize=9.0, color=note_color,
                   family='sans-serif', va='bottom', ha='center')
    
    ax_bottom.set_xlim(0, 1)
    ax_bottom.set_ylim(0, 1)
    
    out_path = 'generated_figures/slide_12_results_and_discussion_full.png'
    fig.savefig(out_path, dpi=300, bbox_inches='tight', facecolor='#ffffff')
    plt.close(fig)
    print(f"Generated {out_path} successfully!")
    return out_path

if __name__ == '__main__':
    generate_metrics_banner()
    generate_full_slide_content()

