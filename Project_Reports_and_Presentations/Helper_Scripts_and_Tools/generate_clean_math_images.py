import matplotlib.pyplot as plt
import os

os.makedirs('patent_figures/equations', exist_ok=True)

plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'STIXGeneral'

equations = [
    ("4.1", r"\mu_{i,k}(t) = \frac{1}{|W|} \sum_{m=0}^{|W|-1} x_{i,k}(t - m)", 6.2, 0.8),
    ("4.2", r"\sigma_{i,k}^2(t) = \frac{1}{|W| - 1} \sum_{m=0}^{|W|-1} \left( x_{i,k}(t - m) - \mu_{i,k}(t) \right)^2", 7.6, 0.9),
    ("4.3", r"z_{i,k}(t) = \frac{x_{i,k}(t) - \mu_{i,k}(t)}{\sigma_{i,k}(t) + \epsilon}", 5.8, 0.8),
    ("4.4", r"\boldsymbol{\Sigma}(t) = \frac{1}{|W| - 1} \sum_{m=0}^{|W|-1} \mathbf{z}_i(t - m) \, \mathbf{z}_i(t - m)^T + \lambda_{\mathrm{reg}} \mathbf{I}", 8.2, 0.9),
    ("4.5", r"D_M(z_i) = \sqrt{\mathbf{z}_i^T \, \boldsymbol{\Sigma}^{-1} \, \mathbf{z}_i}", 5.8, 0.8),
    ("4.6", r"\mathrm{CHDI}(z_i) = 100 \times \exp\left(-\lambda \, D_M(z_i)\right)", 6.5, 0.8),
    ("4.7", r"S = \frac{\sum_{t=1}^k (t - \bar{t})( \mathrm{CHDI}_t - \overline{\mathrm{CHDI}} )}{\sum_{t=1}^k (t - \bar{t})^2}", 7.2, 0.9),
    ("4.8", r"C_k = \frac{D_M(z) - D_M(z_{-k})}{\sum_{j=1}^m \left( D_M(z) - D_M(z_{-j}) \right)} \times 100\%", 7.5, 0.9),
    ("4.9", r"\mathrm{Conf}(N) = \min\left(1.0, \, \frac{N}{N_{\min}}\right), \quad N_{\min} = 7", 6.8, 0.8)
]

for idx, (eq_num, latex_str, w, h) in enumerate(equations, start=1):
    fig = plt.figure(figsize=(w, h), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    
    # Render mathematical text
    ax.text(0.42, 0.5, f"${latex_str}$", fontsize=16, ha='center', va='center', color='black')
    # Render Equation number on right
    ax.text(0.95, 0.5, f"({eq_num})", fontsize=15, ha='right', va='center', color='black', fontfamily='Times New Roman', fontweight='bold')
    
    out_path = f"patent_figures/equations/eq_{idx}.png"
    plt.savefig(out_path, dpi=300, bbox_inches='tight', pad_inches=0.08, transparent=False, facecolor='white')
    plt.close()
    print(f"Generated {out_path} for Equation ({eq_num})")
