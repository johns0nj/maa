import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
rcParams['axes.unicode_minus'] = False

# 定义策略数据
strategies = ['固收', '固收+', 'SAA', 'TAA多资产', '权益-', '权益', '权益+']

# 预期收益率（使用中位数）
expected_returns = [4.0, 4.15, 4.25, 4.45, 6.15, 7.0, 9.0]

# 波动率（标准差，年化）
volatilities = [2.5, 3.5, 4.5, 5.5, 11.0, 16.0, 19.0]

# 策略颜色映射
colors = ['#5B9BD5', '#4472C4', '#70AD47', '#FFC000', '#ED7D31', '#C5504B', '#A5A5A5']

# 创建图表
fig, ax = plt.subplots(figsize=(24, 16))

# 画出各个策略点
scatter = ax.scatter(volatilities, expected_returns, s=800, c=colors, 
                     alpha=0.8, edgecolors='black', linewidths=5, zorder=3)

# 在每个点旁边添加策略名称
for i, strategy in enumerate(strategies):
    offset_x = 0.3
    offset_y = 0.15
    
    # 针对特定策略调整标注位置，避免重叠
    if strategy == '固收':
        offset_x, offset_y = 0.3, 0.2
    elif strategy == '固收+':
        offset_x, offset_y = 0.3, -0.3
    elif strategy == 'SAA':
        offset_x, offset_y = 0.4, 0.2
    elif strategy == 'TAA多资产':
        offset_x, offset_y = 0.4, -0.3
    elif strategy == '权益-':
        offset_x, offset_y = 0.5, 0.2
    elif strategy == '权益':
        offset_x, offset_y = 0.5, -0.3
    elif strategy == '权益+':
        offset_x, offset_y = 0.5, 0.2
    
    ax.annotate(strategy, 
                (volatilities[i], expected_returns[i]),
                xytext=(offset_x, offset_y), 
                textcoords='offset fontsize',
                fontsize=44, 
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                         edgecolor='gray', alpha=0.8, linewidth=2))

# 绘制有效前沿曲线（所有策略点都在曲线上或下方）
# 对数据点进行排序
sorted_indices = np.argsort(volatilities)
vol_sorted = np.array(volatilities)[sorted_indices]
ret_sorted = np.array(expected_returns)[sorted_indices]

# 找到有效前沿上的点（对于每个风险水平，选择最高收益的策略）
# 构建有效前沿：从最左边的点开始，只包含向右上方移动的点
efficient_points = []
max_return = -np.inf

for i in sorted_indices:
    if expected_returns[i] >= max_return:
        efficient_points.append(i)
        max_return = expected_returns[i]

# 提取有效前沿上的点
eff_vol = np.array([volatilities[i] for i in efficient_points])
eff_ret = np.array([expected_returns[i] for i in efficient_points])

# 生成平滑的x轴数据
vol_smooth = np.linspace(max(0.1, eff_vol[0] - 0.5), eff_vol[-1] + 1, 300)

# 使用平方根函数拟合有效前沿：y = a + b*sqrt(x)
# 这符合金融理论中有效前沿的凹函数特性（边际收益递减）
sqrt_eff_vol = np.sqrt(eff_vol)
sqrt_vol_smooth = np.sqrt(vol_smooth)

# 线性拟合 sqrt(vol) vs return (使用有效点)
coeffs = np.polyfit(sqrt_eff_vol, eff_ret, 1)
b, a = coeffs  # y = a + b*sqrt(x)

# 生成有效前沿曲线
ret_smooth = a + b * sqrt_vol_smooth

# 画出有效前沿曲线
ax.plot(vol_smooth, ret_smooth, color='#5B8DB8', linestyle='-', 
        linewidth=7, alpha=0.75, label='有效前沿', zorder=1)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.4, zorder=0)
ax.set_axisbelow(True)

# 设置标签和标题
ax.set_xlabel('波动率（年化标准差，%）', fontsize=56, fontweight='bold', labelpad=15)
ax.set_ylabel('预期收益率（年化，%）', fontsize=56, fontweight='bold', labelpad=15)
ax.set_title('资产配置策略有效前沿', fontsize=68, fontweight='bold', pad=25)

# 设置刻度标签字体大小
ax.tick_params(axis='both', which='major', labelsize=44)

# 设置坐标轴范围
ax.set_xlim(0, max(volatilities) + 2)
ax.set_ylim(min(expected_returns) - 1, max(expected_returns) + 1)

# 添加图例
ax.legend(loc='lower right', fontsize=48, framealpha=0.9)

# 在图表左下角添加说明文字
info_text = '风险收益特征：\n低波动率 → 固收类策略\n高波动率 → 权益及另类策略'
ax.text(0.02, 0.98, info_text, transform=ax.transAxes, 
        fontsize=40, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5, pad=1))

# 计算夏普比率（用于数据表输出）
risk_free_rate = 2.5
sharpe_ratios = [(expected_returns[i] - risk_free_rate) / volatilities[i] 
                 for i in range(len(strategies))]
best_sharpe_idx = np.argmax(sharpe_ratios)

# 调整布局
plt.tight_layout()

# 确保 output 文件夹存在
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 保存图表
output_path = os.path.join(output_dir, 'efficient_frontier.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"有效前沿图表已保存为 '{output_path}'")

# 显示图表
plt.show()

# 打印详细数据表
print("\n" + "="*80)
print("策略风险收益特征：")
print("="*80)
print(f"{'策略名称':<15} {'预期收益率':<12} {'波动率':<10} {'夏普比率':<10}")
print(f"{'':15} {'(%)':<12} {'(%)':<10} {'(无风险率2.5%)':<10}")
print("="*80)
for i, strategy in enumerate(strategies):
    sharpe = (expected_returns[i] - risk_free_rate) / volatilities[i]
    print(f"{strategy:<12} {expected_returns[i]:>8.2f} {volatilities[i]:>13.2f} {sharpe:>16.3f}")
print("="*80)
print(f"\n最优夏普比率策略：{strategies[best_sharpe_idx]} (夏普比率: {sharpe_ratios[best_sharpe_idx]:.3f})")
print("="*80)

