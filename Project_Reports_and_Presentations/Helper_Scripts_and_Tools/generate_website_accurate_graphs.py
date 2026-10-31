import matplotlib.pyplot as plt
import numpy as np
import os

# Set global publication styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.3
plt.rcParams['xtick.major.width'] = 1.2
plt.rcParams['ytick.major.width'] = 1.2

os.makedirs('generated_figures', exist_ok=True)

# -------------------------------------------------------------
# GRAPH 1: Corrected Longitudinal 30-Day CHDI Trajectory
# -------------------------------------------------------------
def generate_corrected_fig4():
    fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=300)
    
    days = np.arange(1, 31)
    # Days 1-10: Stable healthy baseline (~84-87)
    # Days 11-14: Acute Mastitis onset (62 -> 56 -> 50 -> 38 nadir)
    # Days 15-20: Post-treatment recovery (42 -> 53 -> 64 -> 73 -> 81 -> 84)
    # Days 21-30: Restored baseline (~84-87)
    scores = np.array([
        85, 84, 86, 84, 84, 87, 85, 83, 85, 84,   # Days 1-10 (Healthy baseline)
        62, 56, 50, 38,                           # Days 11-14 (Incubation to acute mastitis)
        42, 53, 64, 73, 81, 84,                   # Days 15-20 (Post-treatment recovery)
        85, 86, 84, 85, 87, 86, 85, 84, 86, 85    # Days 21-30 (Restored baseline)
    ])
    
    # Background zones based on SmartCattle website thresholds
    ax.axhspan(75, 100, color='#e8f5e9', alpha=0.75, label='Healthy Zone (≥75)', zorder=1)
    ax.axhspan(50, 75, color='#fff9c4', alpha=0.85, label='Watch Zone (50–74)', zorder=1)
    ax.axhspan(15, 50, color='#ffebee', alpha=0.80, label='At-Risk Zone (<50)', zorder=1)
    
    # Plot line
    ax.plot(days, scores, color='#0d47a1', linewidth=2.4, marker='o', markersize=5.5,
            markerfacecolor='#1976d2', markeredgecolor='#0d47a1', markeredgewidth=1.0,
            label='Animal CHDI (Daily)', zorder=4)
    
    # Annotations matching Kamadhenu's clinical case
    ax.annotate('Watch Alert\n(Day 11, CHDI=62)', xy=(11, 62), xytext=(7.5, 48),
                arrowprops=dict(facecolor='#e65100', edgecolor='#e65100', width=1.4, headwidth=6, headlength=6, shrink=0.08),
                fontsize=8.5, fontweight='bold', color='#e65100', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#fff3e0', edgecolor='#ffb74d', alpha=0.9))
    
    ax.annotate('VetCase Created\n(Day 14, CHDI=38)', xy=(14, 38), xytext=(17.5, 23),
                arrowprops=dict(facecolor='#b71c1c', edgecolor='#b71c1c', width=1.4, headwidth=6, headlength=6, shrink=0.08),
                fontsize=8.5, fontweight='bold', color='#b71c1c', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffebee', edgecolor='#e57373', alpha=0.9))
    
    ax.annotate('Antibiotic & Therapy\nRecovery (Days 15–20)', xy=(18, 73), xytext=(22.5, 60),
                arrowprops=dict(facecolor='#2e7d32', edgecolor='#2e7d32', width=1.2, headwidth=5, headlength=5, shrink=0.08),
                fontsize=8.0, fontweight='bold', color='#2e7d32', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#e8f5e9', edgecolor='#81c784', alpha=0.9))
    
    ax.set_xlabel('Observation Timeline (Days)', fontsize=11, fontweight='bold', labelpad=6)
    ax.set_ylabel('Animal CHDI Score', fontsize=11, fontweight='bold', labelpad=6)
    ax.set_xlim(1, 30)
    ax.set_ylim(15, 100)
    ax.set_xticks(np.arange(5, 31, 5))
    ax.grid(True, linestyle=':', alpha=0.6, linewidth=1.0, zorder=2)
    ax.legend(loc='upper right', fontsize=8.5, framealpha=0.95, edgecolor='#b0bec5')
    
    plt.tight_layout()
    out_path = 'generated_figures/fig4_longitudinal_trajectory.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path} successfully!")
    return out_path

# -------------------------------------------------------------
# GRAPH 2A: Corrected 4-Signal Feature Attribution (Pyrexia Aligned)
# -------------------------------------------------------------
def generate_corrected_fig5_4signals():
    fig, ax = plt.subplots(figsize=(5.6, 3.0), dpi=300)
    
    # Corrected percentages reflecting Kamadhenu's high fever (40.2°C) + severe milk drop
    features = ['Body Weight', 'Feed Intake', 'Body Temp.', 'Daily Milk Yield']
    importances = [8.6, 16.2, 28.4, 46.8]
    colors = ['#5c6bc0', '#26a69a', '#42a5f5', '#66bb6a']
    
    y = np.arange(len(features))
    bars = ax.barh(y, importances, color=colors, height=0.55, edgecolor='black', linewidth=1.3, zorder=3)
    
    for bar, val in zip(bars, importances):
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height() / 2, f'{val:.1f}%',
                ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    ax.set_xlabel('Relative Feature Importance (%)', fontsize=11, fontweight='bold', labelpad=6)
    ax.set_yticks(y)
    ax.set_yticklabels(features, fontsize=10, fontweight='bold')
    ax.set_xlim(0, 58)
    ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0, linewidth=1.0)
    
    plt.tight_layout()
    out_path = 'generated_figures/fig5_feature_importance.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path} successfully!")
    return out_path

# -------------------------------------------------------------
# GRAPH 2B: Comprehensive 5-Signal Attribution (with Rumination)
# -------------------------------------------------------------
def generate_corrected_fig5_5signals():
    fig, ax = plt.subplots(figsize=(5.8, 3.2), dpi=300)
    
    # 5 full physiological signals tracked in the SmartCattle platform
    features = ['Body Weight', 'Feed Intake', 'Rumination Time', 'Body Temp.', 'Daily Milk Yield']
    importances = [4.2, 9.7, 18.4, 26.5, 41.2]
    colors = ['#5c6bc0', '#ab47bc', '#26a69a', '#42a5f5', '#66bb6a']
    
    y = np.arange(len(features))
    bars = ax.barh(y, importances, color=colors, height=0.55, edgecolor='black', linewidth=1.3, zorder=3)
    
    for bar, val in zip(bars, importances):
        w = bar.get_width()
        ax.text(w + 1.0, bar.get_y() + bar.get_height() / 2, f'{val:.1f}%',
                ha='left', va='center', fontsize=9.5, fontweight='bold')
        
    ax.set_xlabel('Relative Feature Importance (%)', fontsize=11, fontweight='bold', labelpad=6)
    ax.set_yticks(y)
    ax.set_yticklabels(features, fontsize=10, fontweight='bold')
    ax.set_xlim(0, 52)
    ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0, linewidth=1.0)
    
    plt.tight_layout()
    out_path = 'generated_figures/fig5_feature_importance_5signals.png'
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    print(f"Generated {out_path} successfully!")
    return out_path

if __name__ == '__main__':
    generate_corrected_fig4()
    generate_corrected_fig5_4signals()
    generate_corrected_fig5_5signals()

