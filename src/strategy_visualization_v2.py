import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams
import os

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
rcParams['axes.unicode_minus'] = False

# 定义策略数据
strategies = ['固收配置策略', 'SAA策略', '外委多资产策略', '权益策略']

# 三类资产占比
fixed_income_ratio = [100, 92, 40, 0]  # 固收占比
equity_ratio = [0, 8, 60, 100]  # 权益占比
alternative_ratio = [0, 0, 0, 0]  # 另类资产占比（商品、黄金等）

# 固收、权益和另类资产的基础预期收益率
fixed_income_return = (3.5, 4.5)  # 固收：3.5%-4.5%
equity_return = (6.0, 8.0)  # 权益：6%-8%
alternative_return = (10.0, 13.0)  # 另类资产：10%-13%（商品、黄金等）

# 定义每个策略的预期收益率区间
return_ranges = []
for i in range(len(strategies)):
    if strategies[i] == '外委多资产策略':  # 外委多资产策略使用固定的5.5%-6.5%
        return_ranges.append('5.5-6.5%')
    else:  # 其他策略根据配置比例计算
        min_return = (fixed_income_ratio[i] / 100) * fixed_income_return[0] + \
                     (equity_ratio[i] / 100) * equity_return[0] + \
                     (alternative_ratio[i] / 100) * alternative_return[0]
        max_return = (fixed_income_ratio[i] / 100) * fixed_income_return[1] + \
                     (equity_ratio[i] / 100) * equity_return[1] + \
                     (alternative_ratio[i] / 100) * alternative_return[1]
        return_ranges.append(f'{min_return:.1f}-{max_return:.1f}%')

# 使用等间距的x轴位置
x_positions = np.arange(len(strategies))

# 创建图表
fig, ax = plt.subplots(figsize=(24, 18))

# 设置柱子宽度
bar_width = 0.6

# 创建堆叠柱状图
bars1 = ax.bar(x_positions, fixed_income_ratio, bar_width, 
               label='固收', color='#5B9BD5', alpha=0.8)
bars2 = ax.bar(x_positions, equity_ratio, bar_width, 
               bottom=fixed_income_ratio, label='权益', 
               color='#ED7D31', alpha=0.8)

# 计算另类资产的bottom位置
alternative_bottom = [fixed_income_ratio[i] + equity_ratio[i] for i in range(len(strategies))]
bars3 = ax.bar(x_positions, alternative_ratio, bar_width, 
               bottom=alternative_bottom, label='另类资产', 
               color='#70AD47', alpha=0.8)

# 在柱子上添加策略名称
for i, (x, strategy, return_range) in enumerate(zip(x_positions, strategies, return_ranges)):
    # 添加策略名称
    ax.text(x, 108, strategy, ha='center', va='bottom', 
            fontsize=44, fontweight='bold')
    
    # 添加收益率区间
    ax.text(x, -10, return_range, ha='center', va='top', 
            fontsize=40, color='#333333')
    
    # 在柱子内添加占比文字
    if fixed_income_ratio[i] > 5:
        ax.text(x, fixed_income_ratio[i]/2, f'{fixed_income_ratio[i]}%', 
                ha='center', va='center', fontsize=40, color='white', fontweight='bold')
    if equity_ratio[i] > 5:
        ax.text(x, fixed_income_ratio[i] + equity_ratio[i]/2, f'{equity_ratio[i]}%', 
                ha='center', va='center', fontsize=40, color='white', fontweight='bold')
    if alternative_ratio[i] > 5:
        ax.text(x, alternative_bottom[i] + alternative_ratio[i]/2, f'{alternative_ratio[i]}%', 
                ha='center', va='center', fontsize=40, color='white', fontweight='bold')

# 设置标签和标题
ax.set_xlabel('收益率区间（年化）', fontsize=52, fontweight='bold', labelpad=15)
ax.set_ylabel('资产配置占比（%）', fontsize=52, fontweight='bold')
ax.set_title('不同策略的资产配置与预期收益率', fontsize=64, fontweight='bold', pad=20)

# 设置y轴范围和刻度
ax.set_ylim(-30, 125)
ax.set_yticks(range(0, 101, 10))

# 设置刻度标签字体大小
ax.tick_params(axis='both', which='major', labelsize=40)

# 设置x轴范围和刻度
ax.set_xlim(-0.5, len(strategies) - 0.5)
ax.set_xticks(x_positions)
ax.set_xticklabels([])  # 隐藏默认x轴标签，因为我们用文字标注了

# 添加网格线
ax.grid(axis='y', linestyle='--', alpha=0.3)
ax.set_axisbelow(True)

# 添加图例
ax.legend(loc='upper left', fontsize=44, framealpha=0.9)

# 在底部添加风险等级标注
ax.text(0.5, -24, '← 低风险', ha='center', fontsize=44, 
        color='#666666', style='italic')
ax.text(len(strategies) - 1.5, -24, '高风险 →', ha='center', fontsize=44, 
        color='#666666', style='italic')

# 添加策略说明（分别用红色和绿色显示）
# 红色部分
ax.text(0.55, 0.02, '★ 红框标注为新策略', 
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=36, fontweight='bold', color='red',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                 edgecolor='red', linewidth=3, alpha=0.9))
# 绿色部分
ax.text(0.78, 0.02, '★ 绿框标注为存量策略', 
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=36, fontweight='bold', color='green',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                 edgecolor='green', linewidth=3, alpha=0.9))

# 调整布局
plt.tight_layout()

# 确保 output 文件夹存在
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 保存图表
output_path = os.path.join(output_dir, 'strategy_allocation_v2.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"图表已保存为 '{output_path}'")

# 显示图表
plt.show()

# 打印详细数据表
print("\n" + "="*90)
print("基础假设：")
print(f"  - 固收资产预期收益率：{fixed_income_return[0]:.1f}% - {fixed_income_return[1]:.1f}%")
print(f"  - 权益资产预期收益率：{equity_return[0]:.1f}% - {equity_return[1]:.1f}%")
print(f"  - 另类资产预期收益率：{alternative_return[0]:.1f}% - {alternative_return[1]:.1f}%（商品、黄金等）")
print("="*90)
print("\n策略详细信息：")
print("="*90)
print(f"{'策略名称':<12} {'固收占比':<10} {'权益占比':<10} {'另类占比':<10} {'预期收益率区间':<15}")
print("="*90)
for i, strategy in enumerate(strategies):
    alt_str = f'{alternative_ratio[i]}%' if alternative_ratio[i] > 0 else '-'
    print(f"{strategy:<10} {fixed_income_ratio[i]:>6}% {equity_ratio[i]:>9}% {alt_str:>9} {return_ranges[i]:>15}")
print("="*90)
print("\n注：外委多资产策略包含60%权益和40%固收，预期收益率为5.5%-6.5%")

