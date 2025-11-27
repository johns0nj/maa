import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import os

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
rcParams['axes.unicode_minus'] = False

# 创建图表
fig, ax = plt.subplots(figsize=(20, 14))

# 定义层次结构
# 顶层节点
top_node = {
    'name': 'TAA',
    'pos': (0.5, 0.9),
    'color': '#4472C4',
    'size': 120
}

# 第一层节点
first_level_nodes = [
    {'name': '固收配置策略', 'pos': (0.15, 0.5), 'color': '#5B9BD5'},
    {'name': '固收交易策略', 'pos': (0.35, 0.5), 'color': '#70AD47'},
    {'name': '权益配置', 'pos': (0.65, 0.5), 'color': '#ED7D31'},
    {'name': '境外TAA调整组合', 'pos': (0.85, 0.5), 'color': '#FFC000'}
]

# 绘制连接线
for node in first_level_nodes:
    # 从顶层节点到第一层节点的连接线
    ax.plot([top_node['pos'][0], node['pos'][0]], 
            [top_node['pos'][1], node['pos'][1]], 
            'k-', linewidth=4, alpha=0.6, zorder=1)

# 绘制顶层节点
top_circle = mpatches.Circle(top_node['pos'], 0.08, 
                             color=top_node['color'], 
                             ec='black', linewidth=4, 
                             zorder=3, alpha=0.9)
ax.add_patch(top_circle)
ax.text(top_node['pos'][0], top_node['pos'][1], top_node['name'],
        ha='center', va='center', fontsize=48, fontweight='bold',
        color='white', zorder=4)

# 绘制第一层节点
for node in first_level_nodes:
    # 绘制矩形框
    rect = mpatches.Rectangle((node['pos'][0] - 0.12, node['pos'][1] - 0.08),
                              0.24, 0.16,
                              facecolor=node['color'],
                              edgecolor='black', linewidth=3,
                              zorder=3, alpha=0.85)
    ax.add_patch(rect)
    
    # 添加文字
    ax.text(node['pos'][0], node['pos'][1], node['name'],
            ha='center', va='center', fontsize=36, fontweight='bold',
            color='white', zorder=4)

# 设置坐标轴
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# 添加标题
ax.text(0.5, 0.98, 'TAA 层次结构图', 
        ha='center', va='top', fontsize=56, fontweight='bold',
        transform=ax.transAxes)

# 调整布局
plt.tight_layout()

# 确保 output 文件夹存在
output_dir = 'output'
os.makedirs(output_dir, exist_ok=True)

# 保存图表
output_path = os.path.join(output_dir, 'taa_hierarchy.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"TAA层次结构图已保存为 '{output_path}'")

# 显示图表
plt.show()

print("\n" + "="*80)
print("TAA 层次结构")
print("="*80)
print(f"顶层：{top_node['name']}")
print("\n第一层子策略：")
for i, node in enumerate(first_level_nodes, 1):
    print(f"  {i}. {node['name']}")
print("="*80)

