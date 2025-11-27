import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import os

# 配置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun']
rcParams['axes.unicode_minus'] = False

# 创建图表 - 更大的画布以适应复杂布局
fig, ax = plt.subplots(figsize=(24, 16))

# 定义层次结构
# 顶层节点 - 使用矩形框（蓝色）
top_node = {
    'name': 'TAA',
    'pos': (0.5, 0.88),
    'color': '#4472C4',  # 深蓝色
    'width': 0.15,
    'height': 0.08
}

# 第一层节点 - 水平排列，根据风险特征分类
# 橙色 = 稳定收益类，蓝色 = 波动类
first_level_nodes = [
    {'name': '固收配置策略', 'pos': (0.15, 0.6), 'color': '#ED7D31'},  # 橙色 - 稳定收益类
    {'name': '固收交易策略', 'pos': (0.35, 0.6), 'color': '#ED7D31'},  # 橙色 - 稳定收益类
    {'name': '权益配置', 'pos': (0.65, 0.6), 'color': '#4472C4'},  # 蓝色 - 波动类
    {'name': '境外TAA调整组合', 'pos': (0.85, 0.6), 'color': '#4472C4'}  # 蓝色 - 波动类
]

# 节点尺寸
node_width = 0.12
node_height = 0.06

# 绘制连接线 - 从顶层到第一层（垂直连接）
for node in first_level_nodes:
    # 垂直线从顶层节点底部到第一层节点顶部
    ax.plot([top_node['pos'][0], node['pos'][0]], 
            [top_node['pos'][1] - top_node['height']/2, node['pos'][1] + node_height/2], 
            'k-', linewidth=3, alpha=0.5, zorder=1)

# 绘制顶层节点 - 矩形框
top_rect = mpatches.Rectangle(
    (top_node['pos'][0] - top_node['width']/2, top_node['pos'][1] - top_node['height']/2),
    top_node['width'], top_node['height'],
    facecolor=top_node['color'],
    edgecolor='black', linewidth=3,
    zorder=3, alpha=0.9
)
ax.add_patch(top_rect)
ax.text(top_node['pos'][0], top_node['pos'][1], top_node['name'],
        ha='center', va='center', fontsize=44, fontweight='bold',
        color='white', zorder=4)

# 绘制第一层节点 - 矩形框
for node in first_level_nodes:
    rect = mpatches.Rectangle(
        (node['pos'][0] - node_width/2, node['pos'][1] - node_height/2),
        node_width, node_height,
        facecolor=node['color'],
        edgecolor='black', linewidth=2.5,
        zorder=3, alpha=0.85
    )
    ax.add_patch(rect)
    
    # 添加文字 - 根据文字长度调整字体大小
    fontsize = 32 if len(node['name']) <= 6 else 28
    ax.text(node['pos'][0], node['pos'][1], node['name'],
            ha='center', va='center', fontsize=fontsize, fontweight='bold',
            color='white', zorder=4)

# 左侧标签区域 - 垂直排列
left_labels = [
    {'text': '配置引领', 'y': 0.75},
    {'text': '策略驱动', 'y': 0.6},
    {'text': '交易协同', 'y': 0.45}
]

for label in left_labels:
    ax.text(0.02, label['y'], label['text'],
            ha='left', va='center', fontsize=32, fontweight='bold',
            color='#333333', transform=ax.transAxes)

# 右侧策略分类说明
strategy_categories = [
    {'name': '稳定收益类', 'pos': (0.92, 0.75), 'color': '#ED7D31'},
    {'name': '波动类', 'pos': (0.92, 0.65), 'color': '#4472C4'}
]

for cat in strategy_categories:
    # 绘制分类节点
    cat_rect = mpatches.Rectangle(
        (cat['pos'][0] - 0.08, cat['pos'][1] - 0.03),
        0.16, 0.06,
        facecolor=cat['color'],
        edgecolor='black', linewidth=2,
        zorder=3, alpha=0.85
    )
    ax.add_patch(cat_rect)
    ax.text(cat['pos'][0], cat['pos'][1], cat['name'],
            ha='center', va='center', fontsize=28, fontweight='bold',
            color='white', zorder=4)

# 添加分类说明文字
category_text = '以风险特征为标准，将策略明确划分为\n稳定收益类和波动类两大类'
ax.text(0.92, 0.55, category_text,
        ha='center', va='top', fontsize=24,
        color='#666666', transform=ax.transAxes,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                 edgecolor='gray', alpha=0.8, linewidth=1))

# 设置坐标轴
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# 添加标题
ax.text(0.5, 0.96, '多策略下的均衡、分散性配置', 
        ha='center', va='top', fontsize=52, fontweight='bold',
        transform=ax.transAxes, color='#1a1a1a')

# 添加层级标签
ax.text(0.5, 0.68, '一级策略', 
        ha='center', va='center', fontsize=28, 
        color='#666666', style='italic', transform=ax.transAxes)

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
print("\n第一层子策略（一级策略）：")
for i, node in enumerate(first_level_nodes, 1):
    category = "稳定收益类" if node['color'] == '#ED7D31' else "波动类"
    print(f"  {i}. {node['name']} ({category})")
print("="*80)
