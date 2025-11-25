import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# 配置中文字体 - 修复中文乱码
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# 确保字体正确加载
import matplotlib
matplotlib.rcParams['font.family'] = 'sans-serif'

# ==================== 基础参数设置 ====================
# 权益参数
stock_return = 7.5  # 预期收益率 (%)
stock_volatility = 18.0  # 波动率 (%)

# 固收参数
bond_return = 4.5  # 预期收益率 (%)
bond_volatility = 7.0  # 波动率 (%)

# 相关系数
correlation = 0.2  # 权益和固收的相关系数

# ==================== 组合计算函数 ====================
def calculate_portfolio(w_stock, w_bond, r_stock, r_bond, vol_stock, vol_bond, corr):
    """
    计算组合的预期收益率和波动率
    
    参数:
    w_stock: 股票权重
    w_bond: 债券权重
    r_stock: 股票预期收益率
    r_bond: 债券预期收益率
    vol_stock: 股票波动率
    vol_bond: 债券波动率
    corr: 相关系数
    
    返回:
    portfolio_return: 组合预期收益率
    portfolio_volatility: 组合波动率
    """
    # 组合预期收益率 = w1*r1 + w2*r2
    portfolio_return = w_stock * r_stock + w_bond * r_bond
    
    # 组合波动率 = sqrt(w1^2*σ1^2 + w2^2*σ2^2 + 2*w1*w2*σ1*σ2*ρ)
    portfolio_variance = (w_stock**2 * vol_stock**2 + 
                         w_bond**2 * vol_bond**2 + 
                         2 * w_stock * w_bond * vol_stock * vol_bond * corr)
    portfolio_volatility = np.sqrt(portfolio_variance)
    
    return portfolio_return, portfolio_volatility

# ==================== 生成不同权重的组合 ====================
# 股票权重从0%到100%
weights_stock = np.linspace(0, 1, 101)
weights_bond = 1 - weights_stock

# 计算每个组合的收益和风险
portfolio_returns = []
portfolio_volatilities = []

for w_s, w_b in zip(weights_stock, weights_bond):
    ret, vol = calculate_portfolio(w_s, w_b, stock_return, bond_return, 
                                   stock_volatility, bond_volatility, correlation)
    portfolio_returns.append(ret)
    portfolio_volatilities.append(vol)

# ==================== 创建可视化 ====================
fig, ax1 = plt.subplots(figsize=(16, 10))

# 绘制有效前沿曲线
ax1.plot(portfolio_volatilities, portfolio_returns, 'b-', linewidth=3, label='有效前沿')

# 标注纯权益和纯固收点
ax1.scatter([bond_volatility], [bond_return], s=400, c='blue', 
           marker='s', edgecolors='black', linewidths=2, zorder=5, label='纯固收')
ax1.annotate(f'纯固收\n收益率: {bond_return}%\n波动率: {bond_volatility}%', 
            xy=(bond_volatility, bond_return), 
            xytext=(15, 15), textcoords='offset points',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', 
                     alpha=0.8, edgecolor='black', linewidth=2))

ax1.scatter([stock_volatility], [stock_return], s=400, c='red', 
           marker='s', edgecolors='black', linewidths=2, zorder=5, label='纯权益')
ax1.annotate(f'纯权益\n收益率: {stock_return}%\n波动率: {stock_volatility}%', 
            xy=(stock_volatility, stock_return), 
            xytext=(15, -25), textcoords='offset points',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', 
                     alpha=0.8, edgecolor='black', linewidth=2))

# 标注几个典型组合：60%权益40%固收，和20%权益80%固收
typical_weights = [0.6, 0.2]
typical_colors = ['green', 'orange']
typical_labels = ['60%权益\n40%固收', '20%权益\n80%固收']
for i, w_s in enumerate(typical_weights):
    w_b = 1 - w_s
    ret, vol = calculate_portfolio(w_s, w_b, stock_return, bond_return, 
                                   stock_volatility, bond_volatility, correlation)
    ax1.scatter([vol], [ret], s=300, c=typical_colors[i], 
               marker='o', edgecolors='black', linewidths=2, zorder=5)
    # 标注组合配置、预期收益率和波动率
    annotation_text = f'{typical_labels[i]}\n收益率: {ret:.2f}%\n波动率: {vol:.2f}%'
    ax1.annotate(annotation_text, 
                xy=(vol, ret), 
                xytext=(15, 15) if i == 0 else (15, -25), 
                textcoords='offset points',
                fontsize=14, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor=typical_colors[i], 
                         alpha=0.8, edgecolor='black', linewidth=2))

ax1.set_xlabel('组合波动率 (%)', fontsize=18, fontweight='bold')
ax1.set_ylabel('组合预期收益率 (%)', fontsize=18, fontweight='bold')
ax1.set_title('固收-权益组合的有效前沿', fontsize=22, fontweight='bold', pad=20)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(fontsize=16, loc='lower right')
ax1.tick_params(axis='both', which='major', labelsize=16)

plt.tight_layout()

# 确保 output 文件夹存在
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 保存图表
output_path = os.path.join(output_dir, 'portfolio_theory.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"投资组合理论可视化已保存为 '{output_path}'")

# 显示图表
plt.show()

# ==================== 打印详细组合数据 ====================
print("\n" + "="*80)
print("不同权益-固收配置的组合特征")
print("="*80)
print(f"{'权益权重':<10} {'固收权重':<10} {'预期收益率(%)':<15} {'波动率(%)':<12}")
print("="*80)

for w_s in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    w_b = 1 - w_s
    ret, vol = calculate_portfolio(w_s, w_b, stock_return, bond_return,
                                   stock_volatility, bond_volatility, correlation)
    print(f"{w_s*100:>8.0f}% {w_b*100:>10.0f}% {ret:>16.2f} {vol:>14.2f}")

print("="*80)
print(f"\n基础假设：")
print(f"  权益: 收益率={stock_return}%, 波动率={stock_volatility}%")
print(f"  固收: 收益率={bond_return}%, 波动率={bond_volatility}%")
print(f"  相关系数={correlation}")
print("="*80)

