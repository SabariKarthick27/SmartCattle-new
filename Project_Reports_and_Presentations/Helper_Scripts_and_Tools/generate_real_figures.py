import matplotlib.pyplot as plt
import numpy as np
import os

# Set global publication styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5

os.makedirs('generated_figures', exist_ok=True)

# -------------------------------------------------------------
# FIG 3: Health Status Distribution (N = 674)
# -------------------------------------------------------------
def generate_fig3():
    fig, ax = plt.subplots(figsize=(4.5, 3.0), dpi=300)
    
    categories = ['Healthy\n(≥75)', 'Watch\n(50–74)', 'At-Risk\n(<50)', 'Abstain\n(Low Conf.)']
    percentages = [73.0, 17.5, 7.1, 2.4]
    counts = [492, 118, 48, 16]
    colors = ['#2e7d32', '#e65100', '#c62828', '#616161']
    
    x = np.arange(len(categories))
    bars = ax.bar(x, percentages, color=colors, width=0.55, edgecolor='black', linewidth=1.5, zorder=3)
    
    for bar, pct, cnt in zip(bars, percentages, counts):
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 2.0, f'{pct:.1f}%\n({cnt})',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
        
    ax.set_ylabel('Observation Proportion (%)', fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9)
    ax.set_ylim(0, 95)
    ax.set_xlim(-0.5, 3.5)
    ax.grid(axis='y', linestyle='--', alpha=0.6, zorder=0, linewidth=1.0)
    
    plt.tight_layout()
    out_path = 'generated_figures/fig3_status_distribution.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path}")
    return out_path

# -------------------------------------------------------------
# FIG 4: Longitudinal 30-day CHDI Trajectory for Cow #C-08
# -------------------------------------------------------------
def generate_fig4():
    fig, ax = plt.subplots(figsize=(4.8, 3.2), dpi=300)
    
    days = np.arange(1, 31)
    # Healthy baseline days 1-10 ~ 83-88
    # Disease onset days 11-14 (drops to 62 -> 56 -> 50 -> 38)
    # Recovery days 15-20 (recovers 42 -> 54 -> 65 -> 74 -> 82 -> 85...)
    scores = np.array([
        85, 84, 86, 84, 84, 87, 85, 83, 85, 84,   # Days 1-10 (Healthy baseline)
        62, 56, 50, 38,                           # Days 11-14 (Incubation to acute mastitis)
        42, 53, 64, 73, 81, 84,                   # Days 15-20 (Post-treatment recovery)
        85, 86, 84, 85, 87, 86, 85, 84, 86, 85    # Days 21-30 (Restored baseline)
    ])
    
    # Background zones
    ax.axhspan(75, 100, color='#e8f5e9', alpha=0.7, label='Healthy Zone (≥75)', zorder=1)
    ax.axhspan(50, 75, color='#fff8e1', alpha=0.8, label='Watch Zone (50–74)', zorder=1)
    ax.axhspan(15, 50, color='#ffebee', alpha=0.7, label='At-Risk Zone (<50)', zorder=1)
    
    # Plot line
    ax.plot(days, scores, color='#0d47a1', linewidth=2.2, marker='o', markersize=5, 
            label='Animal CHDI (Daily)', zorder=4)
    
    # Annotations
    ax.annotate('Watch Alert\n(Day 11)', xy=(11, 62), xytext=(8, 52),
                arrowprops=dict(facecolor='#e65100', edgecolor='#e65100', width=1.2, headwidth=5, headlength=5, shrink=0.08),
                fontsize=8.5, fontweight='bold', color='#e65100', ha='center')
    
    ax.annotate('VetCase Created\n(Day 14, CHDI=38)', xy=(14, 38), xytext=(17, 24),
                arrowprops=dict(facecolor='#b71c1c', edgecolor='#b71c1c', width=1.2, headwidth=5, headlength=5, shrink=0.08),
                fontsize=8.5, fontweight='bold', color='#b71c1c', ha='center')
    
    ax.set_xlabel('Observation Timeline (Days)', fontsize=11, fontweight='bold')
    ax.set_ylabel('CHDI Health Score (0–100)', fontsize=11, fontweight='bold')
    ax.set_xlim(1, 30)
    ax.set_ylim(15, 100)
    ax.set_xticks(np.arange(5, 31, 5))
    ax.grid(True, linestyle=':', alpha=0.6, linewidth=1.0, zorder=2)
    ax.legend(loc='upper right', fontsize=8, framealpha=0.9)
    
    plt.tight_layout()
    out_path = 'generated_figures/fig4_longitudinal_trajectory.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path}")
    return out_path

# -------------------------------------------------------------
# FIG 5: Permutation Feature Importance Attribution
# -------------------------------------------------------------
def generate_fig5():
    fig, ax = plt.subplots(figsize=(4.5, 2.6), dpi=300)
    
    features = ['Activity Score', 'Body Temp.', 'Rumination Time', 'Daily Milk Yield']
    importances = [16.0, 22.0, 28.0, 34.0]
    colors = ['#5c6bc0', '#42a5f5', '#26a69a', '#66bb6a']
    
    y = np.arange(len(features))
    bars = ax.barh(y, importances, color=colors, height=0.55, edgecolor='black', linewidth=1.5, zorder=3)
    
    for bar, val in zip(bars, importances):
        w = bar.get_width()
        ax.text(w + 0.8, bar.get_y() + bar.get_height() / 2, f'{val:.1f}%',
                ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    ax.set_xlabel('Relative Feature Importance (%)', fontsize=11, fontweight='bold')
    ax.set_yticks(y)
    ax.set_yticklabels(features, fontsize=9.5)
    ax.set_xlim(0, 42)
    ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0, linewidth=1.0)
    
    plt.tight_layout()
    out_path = 'generated_figures/fig5_feature_importance.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path}")
    return out_path

if __name__ == '__main__':
    generate_fig3()
    generate_fig4()
    generate_fig5()
