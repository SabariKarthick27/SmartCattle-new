import matplotlib.pyplot as plt
import numpy as np
import os

# Set global publication styling matching the document
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['ytick.major.size'] = 5

os.makedirs('generated_figures', exist_ok=True)

fig, ax = plt.subplots(figsize=(5.2, 2.8), dpi=300)

features = ['Body Weight', 'Body Temp.', 'Feed Intake', 'Daily Milk Yield']
importances = [5.6, 11.8, 28.4, 54.2]
colors = ['#5c6bc0', '#42a5f5', '#26a69a', '#66bb6a']

y = np.arange(len(features))
bars = ax.barh(y, importances, color=colors, height=0.55, edgecolor='black', linewidth=1.5, zorder=3)

for bar, val in zip(bars, importances):
    w = bar.get_width()
    ax.text(w + 1.0, bar.get_y() + bar.get_height() / 2, f'{val:.1f}%',
            ha='left', va='center', fontsize=9.5, fontweight='bold')
    
ax.set_xlabel('Relative Feature Importance (%)', fontsize=11, fontweight='bold')
ax.set_yticks(y)
ax.set_yticklabels(features, fontsize=9.5, fontweight='bold')
ax.set_xlim(0, 65)
ax.grid(axis='x', linestyle='--', alpha=0.6, zorder=0, linewidth=1.0)

plt.tight_layout()
out_path = 'generated_figures/fig5_feature_importance_correct_4signals.png'
fig.savefig(out_path, dpi=300)
plt.close(fig)
print(f"Generated {out_path} successfully!")
