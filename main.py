import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.components import Table

title='一月支出分布'

# 读取Excel文件
input_file = '/Users/laosiyao/Downloads/iCost_20250228151802.xlsx'
df = pd.read_excel(input_file)

# 筛选出类型为“支出”的条目
expenses_df = df[df['类型'] == '支出'].copy()

# 取金额的绝对值（因为支出金额为负数）
expenses_df.loc[:, '金额'] = expenses_df['金额'].abs()



# 按一级分类分组，计算每个分类的总金额
category_sum = expenses_df.groupby('一级分类')['金额'].sum().round(2)
# 计算总支出
total_expense = expenses_df['金额'].sum()
# 格式化总支出
def format_currency(amount):
    return f"￥{amount:,.0f}"  # 格式化为 "￥10,000" 的形式

formatted_total = format_currency(total_expense)

# 将分组结果转换为列表，供 Pyecharts 使用
data = list(zip(category_sum.index, category_sum.values))


# 创建一个字典，存储每个分类的明细表格
category_details = {}
for category, group in expenses_df.groupby('一级分类'):
    table = Table()
    table.add(headers=["日期", "金额", "备注"], rows=group[['日期', '金额', '备注']].values.tolist())
    category_details[category] = table.render_embed()  # 将表格渲染为 HTML 字符串

# 创建饼状图
pie = Pie()

# 添加数据
pie.add(
    "支出分类",
    data,
    radius=["35%", "60%"],  # 设置饼图大小
    # rosetype="radius",       # 设置为南丁格尔图（可选）
)

# 设置全局配置
pie.set_global_opts(
    # title_opts=opts.TitleOpts(title=title, pos_left="center"),
    title_opts=opts.TitleOpts(
        title="总支出",  # 主标题
        subtitle=formatted_total,  # 副标题
        pos_left="center",  # 居中对齐
        pos_top="center",  # 居中对齐
    ),
    legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"),
)



# 设置系列配置
pie.set_series_opts(
    label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),  # 显示分类名称、数值和百分比

)

# # 渲染图表
# pie.render("支出分类饼状图.html")  # 保存为 HTML 文件
# 渲染图表
html_content = f"""
<html>
<head>
    <title>支出分类分布</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.2/dist/echarts.min.js"></script>
    <style>
        #details {{
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            background-color: #f9f9f9;
        }}
    </style>
    <meta charset="UTF-8">
</head>
<body>
    <div id="chart" style="width: 800px; height: 600px;"></div>  <!-- 饼图容器 -->
    <div id="details">点击饼图查看支出明细</div>  <!-- 用于显示明细的区域 -->
    <script>
        // 初始化图表
        var myChart = echarts.init(document.getElementById('chart'));
        var option = {pie.dump_options_with_quotes()};  // 获取饼图配置
        myChart.setOption(option);  // 渲染饼图

        // 监听饼图的点击事件
        myChart.on('click', function(params) {{
            var category = params.name;  // 获取点击的分类名称
            var details = {category_details};  // 获取分类明细表格
            document.getElementById('details').innerHTML = details[category] || '无明细数据';  // 更新网页内容
        }});
    </script>
</body>
</html>
"""

# 将 HTML 内容写入文件
with open("./202501.html", "w", encoding="utf-8") as f:
    f.write(html_content)
