import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import cm

# 确保中文显示正常
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 读取数据
def load_data(file_path):
    return pd.read_csv(file_path)

# 绘制按月份交易金额柱状图
def draw_monthly_trade_amount(df, result_path):
    df['month'] = pd.to_datetime(df['OCCTIME']).dt.month
    df_month = df.groupby('month')['TRANAMT'].sum()
    df_month = df_month.sort_index()

    plt.figure(figsize=(len(df_month) * 1, 6))
    colors = cm.jet(df_month / df_month.max())
    df_month.plot(kind='bar', color=colors, title='2024年校园卡分月交易金额', rot=0)
    plt.xlabel('月份')
    plt.ylabel('交易金额')
    plt.tight_layout()  # 自动去除不必要的空白区域
    plt.savefig(os.path.join(result_path, 'monthly_trade_amount.png'))
    plt.close()

# 绘制按地点交易金额柱状图
def draw_location_trade_amount(df, result_path):
    df_location = df.groupby('MERCNAME')['TRANAMT'].sum().sort_values()
    plt.figure(figsize=(18, 8))
    colors = cm.cool(df_location / df_location.max())
    df_location.plot(kind='barh', color=colors, title='2024年校园卡分窗口交易金额')
    for i, (name, value) in enumerate(zip(df_location.index, df_location)):
        plt.text(value + 0.5, i, f'{value:.2f}', ha='left', va='center', fontsize=10)
    plt.xlabel('交易金额')
    plt.ylabel('消费地点')
    plt.tight_layout()  # 自动去除不必要的空白区域
    plt.savefig(os.path.join(result_path, 'location_trade_amount.png'))
    plt.close()


def draw_window_trade_amount(df, result_path):
    # 按CANTEEN列分组，计算每个地点的交易金额总和
    df_window = df.groupby('CANTEEN')['TRANAMT'].sum()
    df_window = df_window.sort_values()

    # 绘制横向柱状图
    plt.figure(figsize=(10,len(df_window) * 0.4))

    # 设置颜色按金额变化
    colors = plt.cm.spring(df_window / df_window.max())

    # 绘制柱状图
    df_window.plot(kind='barh', title=f'2024年校园卡分地点交易金额', fontsize=8,rot=0, color=colors)

    # 绘制每个食堂的交易金额标签
    for i, (amount, label) in enumerate(zip(df_window, df_window.index)):
        plt.text(amount + 0.5, i, f'{amount:.2f}', ha='left', va='center', fontsize=8)

    plt.ylabel('地点')
    plt.tight_layout()  # 自动去除不必要的空白区域
    # 保存图像到指定路径
    plt.savefig(os.path.join(result_path,f'2024年分地点校园卡交易金额.png'))
    # plt.show()  # 如果你希望直接显示图像可以取消注释这一行

# 绘制按小时交易金额柱状图
def draw_hourly_trade_amount(df, result_path):
    df['hour'] = pd.to_datetime(df['OCCTIME']).dt.hour
    df_hour = df.groupby('hour')['TRANAMT'].sum()
    plt.figure(figsize=(10, 6))
    colors = cm.jet(df_hour / df_hour.max())
    df_hour.plot(kind='bar', color=colors, title='2024年校园卡分时间交易金额', rot=0)
    plt.xlabel('小时')
    plt.ylabel('交易金额')
    plt.tight_layout()  # 自动去除不必要的空白区域
    plt.savefig(os.path.join(result_path, 'hourly_trade_amount.png'))
    plt.close()

def draw_hourly_trade_amount_pie(df, result_path):
    df['hour'] = pd.to_datetime(df['OCCTIME']).dt.hour
    df_hour = df.groupby('hour')['TRANAMT'].sum()

    # 去掉较小的小时交易金额
    threshold = df_hour.max() * 0.02  # 设置阈值
    df_hour = df_hour[df_hour > threshold]
    other = df_hour[df_hour <= threshold].sum()
    df_hour = df_hour[df_hour > threshold]
    df_hour['Other'] = other

    # 增加图表大小，调整显示效果
    plt.figure(figsize=(6, 6))
    colors = cm.jet(np.linspace(0, 1, len(df_hour)))
    df_hour.plot(kind='pie', autopct='%1.1f%%', colors=colors, title='2024年校园卡分时间交易金额', wedgeprops={'width': 0.3})
    plt.ylabel('')
    plt.tight_layout()  # 自动去除不必要的空白区域

    # 保存图像
    plt.savefig(os.path.join(result_path, 'hourly_trade_amount_pie.png'))
    plt.close()

# 绘制按地点交易金额饼图
def draw_location_trade_amount_pie(df, result_path):
    df_location = df.groupby('MERCNAME')['TRANAMT'].sum()
    plt.figure(figsize=(8, 8))
    colors = cm.jet(np.linspace(0, 1, len(df_location)))
    df_location.plot(kind='pie', autopct='%1.1f%%', colors=colors, title='2024年校园卡分窗口交易金额')
    plt.ylabel('')
    plt.tight_layout()  # 自动去除不必要的空白区域
    plt.savefig(os.path.join(result_path, 'location_trade_amount_pie.png'))
    plt.close()


def draw_location_trade_count(df, result_path):
    # 按CANTEEN列统计每个地点的交易次数
    df_canteen_count = df['CANTEEN'].value_counts()
    if 'A17公寓' in df_canteen_count:
        df_canteen_count['A17公寓'] = df_canteen_count['A17公寓'] // 3
    df_canteen_count = df_canteen_count.sort_values(ascending=True)

    # 绘制横向柱状图
    plt.figure(figsize=(14, len(df_canteen_count) * 0.4))

    # 设置颜色变化
    colors = plt.cm.jet(np.linspace(0, 1, len(df_canteen_count)))

    # 绘制柱状图
    df_canteen_count.plot(kind='barh', title=f'2024年校园卡地点交易总次数排行', rot=0, color=colors)

    # 绘制每个地点的交易次数标签
    for i, (count, label) in enumerate(zip(df_canteen_count, df_canteen_count.index)):
        plt.text(count + 0.5, i, f'{count}次', ha='left', va='center', fontsize=8)

    # 设置y轴标签
    plt.ylabel('地点')
    plt.tight_layout()  # 自动去除不必要的空白区域
    # 保存图像到指定路径
    plt.savefig(os.path.join(result_path,f'2024年校园卡地点交易总次数排行.png'))
    # plt.show()  # 如果需要显示图像，可以取消注释这一行


def draw_window_trade_count(df, result_path):
    # 按MERCNAME列统计每个窗口（商户名称）的交易次数
    df_name_count = df['MERCNAME'].value_counts()
    if 'A17公寓浴池' in df_name_count:
        df_name_count['A17公寓浴池'] = df_name_count['A17公寓浴池'] // 3
    df_name_count = df_name_count.sort_values(ascending=True)

    # 可选：只取前20个窗口的次数（如果需要可以取消注释）
    # df_name_count = df_name_count.head(20)

    # 绘制横向柱状图
    plt.figure(figsize=(18, 8))

    # 设置颜色变化
    colors = plt.cm.jet(np.linspace(0, 1, len(df_name_count)))

    # 绘制柱状图
    df_name_count.plot(kind='barh', title=f'2024年校园卡交易窗口总次数排行', rot=0, color=colors)

    # 绘制每个窗口的交易次数标签
    for i, (count, label) in enumerate(zip(df_name_count, df_name_count.index)):
        plt.text(count + 0.5, i, f'{count}次', ha='left', va='center', fontsize=8)

    # 设置y轴标签
    plt.ylabel('窗口')

    # 保存图像到指定路径
    plt.savefig(os.path.join(result_path,f'2024年校园卡交易窗口总次数排行top20.png'))
    # plt.show()  # 如果需要显示图像，可以取消注释这一行

# 处理餐次数据
def get_meal_data(df):
    # 排除CANTEEN内容为"A17公寓"和"宝宝巴士"的记录
    df = df[~df['CANTEEN'].isin(['A17公寓', '宝宝巴士'])]

    # 转换OCCTIME为datetime格式并提取小时
    df['OCCTIME'] = pd.to_datetime(df['OCCTIME'])
    df['hour'] = df['OCCTIME'].dt.hour

    # 餐次划分
    df_breakfast = df[(df['hour'] >= 4) & (df['hour'] <= 9)]
    df_lunch = df[(df['hour'] >= 10) & (df['hour'] <= 13)]
    df_dinner = df[(df['hour'] >= 16) & (df['hour'] <= 19)]
    df_midnight = df[(df['hour'] >= 20) & (df['hour'] <= 23)]

    return df_breakfast, df_lunch, df_dinner, df_midnight

def draw_meal_canteen_count(df, result_path):
    # 获取餐次数据
    df_breakfast, df_lunch, df_dinner, df_midnight = get_meal_data(df)

    # 按CANTEEN统计次数
    df_breakfast_addr = df_breakfast['CANTEEN'].value_counts().head(3)
    df_lunch_addr = df_lunch['CANTEEN'].value_counts().head(3)
    df_dinner_addr = df_dinner['CANTEEN'].value_counts().head(3)
    df_midnight_addr = df_midnight['CANTEEN'].value_counts().head(3)

    # 合并统计结果
    df_addr_count = pd.concat([df_breakfast_addr, df_lunch_addr, df_dinner_addr, df_midnight_addr], axis=1)
    df_addr_count.columns = ['早餐', '午饭', '晚饭', '宵夜']
    df_addr_count = df_addr_count.fillna(0).T

    # 绘制柱状图
    colors = plt.cm.jet(np.linspace(0, 1, len(df_addr_count.columns)))
    ax = df_addr_count.plot(kind='bar', figsize=(12, 6), title=f'2024年校园卡早餐、午饭、晚饭、宵夜常去的食堂次数排行',
                            rot=0, color=colors)

    # 添加标签
    for p in ax.patches:  # ax.patches 是每个柱状图的矩形对象
        height = p.get_height()  # 获取柱的高度
        x = p.get_x() + p.get_width() / 2  # 获取柱的中心位置
        if height > 0:  # 仅当柱的高度大于0时添加标签
            ax.text(x, height + 0.5, f'{int(height)}', ha='center', va='bottom', fontsize=8)

    # 保存图像
    plt.legend(title='食堂')
    plt.xlabel('餐次')
    plt.ylabel('次数')
    plt.savefig(os.path.join(result_path,f'2024年校园卡早餐午饭晚饭宵夜常去食堂次数排行.png'))
    plt.close()

# 绘制餐次常去的窗口的次数柱状图
def draw_meal_window_count(df, result_path):
    # 获取餐次数据
    df = df[~df['MERCNAME'].isin(['深澜网费对接'])]
    df_breakfast, df_lunch, df_dinner, df_midnight = get_meal_data(df)

    # 按MERCNAME统计次数
    df_breakfast_name = df_breakfast['MERCNAME'].value_counts().head(3)
    df_lunch_name = df_lunch['MERCNAME'].value_counts().head(3)
    df_dinner_name = df_dinner['MERCNAME'].value_counts().head(3)
    df_midnight_name = df_midnight['MERCNAME'].value_counts().head(3)

    # 合并统计结果
    df_name_count = pd.concat([df_breakfast_name, df_lunch_name, df_dinner_name, df_midnight_name], axis=1)
    df_name_count.columns = ['早餐', '午饭', '晚饭', '宵夜']
    df_name_count = df_name_count.fillna(0).T

    # 绘制柱状图
    colors = plt.cm.jet(np.linspace(0, 1, len(df_name_count.columns)))
    ax = df_name_count.plot(kind='bar', title=f'2024年校园卡早餐、午饭、晚饭、宵夜常去的窗口次数排行', rot=0, color=colors,
                            figsize=(12, 6))

    # 添加标签
    for p in ax.patches:  # ax.patches 是每个柱状图的矩形对象
        width = p.get_width()  # 获取柱的宽度
        height = p.get_height()  # 获取柱的高度
        x, y = p.get_xy()  # 获取柱的左下角坐标
        if height > 0:  # 仅在柱高度大于 0 时添加标签
            ax.text(x + width / 2, y + height + 0.1, f'{int(height)}', ha='center', va='bottom', fontsize=8)

    # 保存图像
    plt.legend(title='窗口')
    plt.xlabel('餐次')
    plt.ylabel('次数')
    plt.savefig(os.path.join(result_path,f'2024年校园卡早餐午饭晚饭宵夜常去窗口次数排行.png'))
    plt.close()



# 主函数
def main():
    file_path = 'AnnNew.csv'  # 替换为你的文件路径
    result_path = './results'
    os.makedirs(result_path, exist_ok=True)

    df = load_data(file_path)
    # 去除充值
    df = df[df['TRANAMT']<0]
    df['TRANAMT'] = df['TRANAMT'].abs()
    draw_monthly_trade_amount(df, result_path)
    draw_location_trade_amount(df, result_path)
    draw_window_trade_amount(df, result_path)
    draw_hourly_trade_amount(df, result_path)
    draw_hourly_trade_amount_pie(df, result_path)
    draw_location_trade_amount_pie(df, result_path)
    draw_meal_canteen_count(df, result_path)
    draw_meal_window_count(df, result_path)
    draw_location_trade_count(df, result_path)
    draw_window_trade_count(df, result_path)
    draw_meal_canteen_count(df, result_path)
    draw_meal_window_count(df, result_path)
    print('所有图表已生成并保存至', result_path)

if __name__ == '__main__':
    main()
