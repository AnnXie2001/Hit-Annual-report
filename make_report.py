import pandas as pd
import os
from datetime import timedelta


if __name__ == '__main__':
    year = "2024"

    # 创建结果文件夹
    result_path = f'./results/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
        print(f'创建文件夹 {result_path}.')

    username = '24S136027'

    # 读取处理过的有效信息表格
    df_data = pd.read_csv('./AnnNew.csv')
    df_data = df_data[df_data['TRANAMT'] < 0]
    df_data['TRANAMT'] = df_data['TRANAMT'].abs()


    # 生成Markdown标题
    tilte = f"# 哈工小{year}年校园卡年度总结"

    sub_title_0 = f"## 0.申明\n"
    sub_title_0_content = f"""
> 项目数据获取主体框架来源于[Ze-en Xiong](https://github.com/leverimmy)。

> 项目的 idea 来源于 [Rose-max111](https://github.com/Rose-max111)。

> 项目的数据分析与展示制作由我[Ann Xie](https://github.com/AnnXie2001)完成。
    """
    # 总览
    # 获取数据
    # 在校园卡上的总消费金额与次数

    total_spent = df_data['TRANAMT'].sum()
    visit_count =len(df_data)

    # 最常去的食堂
    df_filtered = df_data[~df_data['CANTEEN'].isin(['A17公寓', '宝宝巴士'])]

    # 按CANTEEN统计次数并返回排名
    canteen_counts = df_filtered['CANTEEN'].value_counts()

    most_visited_canteen = canteen_counts.index[0]
    most_visited_canteen_count = canteen_counts.values[0]
    most_visited_canteen_spent = df_filtered[df_filtered['CANTEEN'] == most_visited_canteen]['TRANAMT'].sum()

    # 最常去的窗口
    excluded_windows = ['A17公寓浴池', '校园车载POS', '深澜网费对接']
    df_filtered2 = df_data[~df_data['MERCNAME'].isin(excluded_windows)]
    # 按MERCNAME统计次数
    window_counts = df_filtered2['MERCNAME'].value_counts()

    most_visited_window = window_counts.index[0]
    most_visited_window_count = window_counts.values[0]
    most_visited_window_spent = df_filtered2[df_filtered2['MERCNAME'] == most_visited_window]['TRANAMT'].sum()


    #累计消费最多的食堂
    canteen_stats = df_filtered2.groupby('CANTEEN').agg(
        total_spending=('TRANAMT', 'sum'),
        total_visits=('CANTEEN', 'count')
    )
    most_spent_canteen = canteen_stats['total_spending'].idxmax()
    most_spent_canteen_count = canteen_stats.loc[most_spent_canteen, 'total_visits']
    most_spent_canteen_spent = canteen_stats.loc[most_spent_canteen, 'total_spending']

    #累计消费最多的窗口
    window_stats = df_filtered.groupby('MERCNAME').agg(
        total_spending=('TRANAMT', 'sum'),
        total_visits=('MERCNAME', 'count')
    )
    most_spent_window = window_stats['total_spending'].idxmax()
    most_spent_window_count = window_stats.loc[most_spent_window, 'total_visits']
    most_spent_window_spent = window_stats.loc[most_spent_window, 'total_spending']

    #单次交易金额最大值
    max_transaction = df_data['TRANAMT'].max()

    # 筛选出最大交易金额的记录
    max_transaction_row = df_data[df_data['TRANAMT'] == max_transaction].iloc[0]  # 取第一条记录

    # 提取交易信息
    max_transaction_details = {
        "交易金额": max_transaction_row['TRANAMT'],
        "交易窗口": max_transaction_row['MERCNAME'],
        "交易时间": max_transaction_row['OCCTIME'],
        "交易地点": max_transaction_row['CANTEEN']
    }
    max_spent_for_one_time = max_transaction_details['交易金额']
    max_spent_for_one_time_time = max_transaction_details['交易窗口']
    max_spent_for_one_time_location = max_transaction_details['交易地点']

    #单次交易金额最小值
    min_transaction = df_data['TRANAMT'].min()

    # 筛选出最小交易金额的记录
    min_transaction_row = df_data[df_data['TRANAMT'] == min_transaction].iloc[0]  # 取第一条记录

    # 提取交易信息
    min_transaction_details = {
        "交易金额": min_transaction_row['TRANAMT'],
        "交易窗口": min_transaction_row['MERCNAME'],
        "交易时间": min_transaction_row['OCCTIME'],
        "交易地点": min_transaction_row['CANTEEN']
    }
    min_spent_for_one_time = min_transaction_details['交易金额']
    min_spent_for_one_time_time = min_transaction_details['交易窗口']
    min_spent_for_one_time_location = min_transaction_details['交易地点']

    #交易金额平均值
    average_spent =  df_data['TRANAMT'].mean()

    #交易金额分月最大值与最小值
    df_data['OCCTIME'] = pd.to_datetime(df_data['OCCTIME'])

    # 提取月份
    df_data['Month'] = df_data['OCCTIME'].dt.month

    # 按月份分组计算累计交易金额
    monthly_cumulative = df_data.groupby('Month')['TRANAMT'].sum()

    # 找出累计交易金额的最大值和最小值以及对应的月份
    max_month = monthly_cumulative.idxmax()  # 获取累计金额最大值对应的月份
    max_value = monthly_cumulative.max()  # 获取累计金额最大值
    min_month = monthly_cumulative.idxmin()  # 获取累计金额最小值对应的月份
    min_value = monthly_cumulative.min()  # 获取累计金额最小值

    # 返回结果
    month_transaction_details = {
        "累计金额最大值": max_value,
        "累计金额最大值对应月份": max_month,
        "累计金额最小值": min_value,
        "累计金额最小值对应月份": min_month
    }

    max_spent_month = month_transaction_details['累计金额最大值对应月份']
    max_spent_month_cost = month_transaction_details['累计金额最大值']
    min_spent_month = month_transaction_details['累计金额最小值对应月份']
    min_spent_month_cost = month_transaction_details['累计金额最小值']

    #交易金额分地点最大值与最小值
    cumulative_by_location = df_data.groupby('CANTEEN')['TRANAMT'].sum()

    # 找出累计交易金额的最大值和最小值及其对应地点
    max_location = cumulative_by_location.idxmax()  # 获取累计金额最大值对应的地点
    max_value = cumulative_by_location.max()  # 获取累计金额最大值
    min_location = cumulative_by_location.idxmin()  # 获取累计金额最小值对应的地点
    min_value = cumulative_by_location.min()  # 获取累计金额最小值

    # 返回结果
    place_transaction_details = {
        "累计金额最大值": max_value,
        "最大值对应地点": max_location,
        "累计金额最小值": min_value,
        "最小值对应地点": min_location
    }

    max_spent_location = place_transaction_details['最大值对应地点']
    max_spent_location_cost = place_transaction_details['累计金额最大值']
    min_spent_location = place_transaction_details['最小值对应地点']
    min_spent_location_cost = place_transaction_details['累计金额最小值']

    #交易金额分hour累计最大值与最小值
    df_data['OCCTIME'] = pd.to_datetime(df_data['OCCTIME'])

    # 提取小时
    df_data['Hour'] = df_data['OCCTIME'].dt.hour

    # 按小时分组计算累计交易金额
    cumulative_by_hour = df_data.groupby('Hour')['TRANAMT'].sum()

    # 找出累计交易金额的最大值和最小值及其对应小时
    max_hour = cumulative_by_hour.idxmax()  # 获取累计金额最大值对应的小时
    max_value = cumulative_by_hour.max()  # 获取累计金额最大值
    min_hour = cumulative_by_hour.idxmin()  # 获取累计金额最小值对应的小时
    min_value = cumulative_by_hour.min()  # 获取累计金额最小值

    # 返回结果
    hour_transaction_details = {
        "累计金额最大值": max_value,
        "最大值对应小时": max_hour,
        "累计金额最小值": min_value,
        "最小值对应小时": min_hour
    }
    max_spent_hour = hour_transaction_details['最大值对应小时']
    max_spent_hour_cost = hour_transaction_details['累计金额最大值']
    min_spent_hour = hour_transaction_details['最小值对应小时']
    min_spent_hour_cost = hour_transaction_details['累计金额最小值']

    #分天交易金额最大值与最小值
    df_data['Day'] = df_data['OCCTIME'].dt.date

    # 按天分组计算累计交易金额
    cumulative_by_day = df_data.groupby('Day')['TRANAMT'].sum()

    # 找出累计交易金额的最大值和最小值及其对应日期
    max_day = cumulative_by_day.idxmax()  # 获取累计金额最大值对应的日期
    max_value = cumulative_by_day.max()  # 获取累计金额最大值
    min_day = cumulative_by_day.idxmin()  # 获取累计金额最小值对应的日期
    min_value = cumulative_by_day.min()  # 获取累计金额最小值

    # 返回结果
    day_transaction_details =  {
        "累计金额最大值": max_value,
        "最大值对应日期": max_day,
        "累计金额最小值": min_value,
        "最小值对应日期": min_day
    }

    max_spent_day = day_transaction_details["最大值对应日期"]
    max_spent_day_cost = day_transaction_details["累计金额最大值"]
    min_spent_day = day_transaction_details["最小值对应日期"]
    min_spent_day_cost = day_transaction_details["累计金额最小值"]

    #去过的食堂与窗口
    unique_canteens = df_filtered['CANTEEN'].dropna().unique()  # 去重并排除空值
    unique_windows = df_filtered2['MERCNAME'].dropna().unique()  # 去重并排除空值

    canteen_count = len(unique_canteens)
    canteen_list = list(unique_canteens)

    window_count = len(unique_windows)
    window_list = list(unique_windows)

    

    sub_title_1 = f"## 1.总览\n"
    sub_title_1_content = f"""
{year}年， **{username}** 在哈工小校园卡上共消费 **{total_spent:.2f}** 元， **{visit_count}** 次交易成功，\n
其中最常去的食堂是 **{most_visited_canteen}** ，共消费 **{most_visited_canteen_spent:.2f}** 元， **{most_visited_canteen_count}** 次到访；\n
最常去的窗口是 **{most_visited_window}** ，共消费 **{most_visited_window_spent:.2f}** 元， **{most_visited_window_count}** 次到访。\n
![图片]({result_path}2024年校园卡地点交易总次数排行.png) \n
![图片]({result_path}2024年校园卡交易地点总次数排行.png) \n
![图片]({result_path}2024年校园卡交易窗口总次数排行top20.png) \n

累计消费最多的食堂是 **{most_spent_canteen}** ，共消费 **{most_spent_canteen_spent:.2f}** 元；\n
累计消费最多的窗口是 **{most_spent_window}** ，共消费 **{most_spent_window_spent:.2f}** 元。\n
![图片]({result_path}2024年分地点校园卡交易金额.png) \n
![图片]({result_path}2024年分窗口校园卡交易金额.png) \n

在 **{max_spent_for_one_time_time}** 时，你为了 **{max_spent_for_one_time_location}** 进行了{year}年最大的一笔消费，花了 **{max_spent_for_one_time:.2f}** 元；\n
在 **{min_spent_for_one_time_time}** 时，你进行了{year}年最小的一笔消费，花了 **{min_spent_for_one_time:.2f}** 元。\n

你{year}年平均每次刷校园卡花费 **{average_spent:.2f}** 元。\n\n

还记得 **{max_spent_month}** 月发生了什么吗，你在这个月消费最多，共消费了 **{max_spent_month_cost:.2f}** 元；\n
一个月的时间太长，那你还记得 **{max_spent_day}** 发生了什么吗，你在这一天消费最多，共消费了 **{max_spent_day_cost:.2f}** 元。\n
另外 **{min_spent_month}** 月是不是已经放假回家，你在这个月只消费了 **{min_spent_month_cost:.2f}** 元。\n    
同时，你在有消费的日子中 **{min_spent_day}** 消费最少，只花了 **{min_spent_day_cost:.2f}** 元。\n
![图片]({result_path}2024年分月校园卡交易金额.png) \n

{year}年，你每天最喜欢在 **{max_spent_hour}** 点刷卡，共消费了 **{max_spent_hour_cost:.2f}** 元；\n
你在 **{min_spent_hour}** 点刷卡最少，只花了 **{min_spent_hour_cost:.2f}** 元。\n
![图片]({result_path}2024年分时间校园卡交易金额图.png) \n
    
你这一年里一共去过 **{canteen_count}**个食堂，**{window_count}**个窗口。\n
分别这些食堂分别是 **{canteen_list}** \n

"""
    if canteen_count >= 10:
        sub_title_1_content += f"去过如此之多的食堂，堪称哈工小干饭王！ \n"
    elif canteen_count < 5:
        sub_title_1_content += f"才去了{canteen_count}个食堂，是不是该多尝试一下其他食堂呢？ \n"
    else:
        sub_title_1_content += f"哈工小之大，等你继续探索！ \n"
    
    # 早餐
    # 获取数据
    excluded_windows = ['A17公寓浴池', '校园车载POS', '深澜网费对接']
    df_filtered2 = df_data[~df_data['MERCNAME'].isin(excluded_windows)]
    # 筛选出早餐时间段（4:00-9:59）
    df_breakfast = df_filtered2[(df_filtered2['Hour'] >= 4) & (df_filtered2['Hour'] < 10)]

    # 总次数和总金额
    total_breakfast_count = len(df_breakfast)
    total_breakfast_amount = df_breakfast['TRANAMT'].sum()

    # 常去的食堂（次数最多）
    frequent_canteen = df_breakfast['CANTEEN'].value_counts().idxmax()
    frequent_canteen_count = df_breakfast['CANTEEN'].value_counts().max()
    frequent_canteen_amount = df_breakfast[df_breakfast['CANTEEN'] == frequent_canteen]['TRANAMT'].sum()

    # 常去的窗口（次数最多）
    frequent_window = df_breakfast['MERCNAME'].value_counts().idxmax()
    frequent_window_count = df_breakfast['MERCNAME'].value_counts().max()
    frequent_window_amount = df_breakfast[df_breakfast['MERCNAME'] == frequent_window]['TRANAMT'].sum()

    df_breakfast['Hour'] = df_breakfast['OCCTIME'].dt.hour
    df_breakfast['Adjusted_Hour'] = df_breakfast['Hour'].apply(lambda x: x + 24 if x < 6 else x)

    # 最早吃早餐的记录
    earliest_breakfast = df_breakfast.loc[df_breakfast['Adjusted_Hour'].idxmin()]
    earliest_time = earliest_breakfast['OCCTIME']
    earliest_amount = earliest_breakfast['TRANAMT']
    earliest_canteen = earliest_breakfast['CANTEEN']

    # 最晚吃早餐的记录
    latest_breakfast = df_breakfast.loc[df_breakfast['Adjusted_Hour'].idxmax()]
    latest_time = latest_breakfast['OCCTIME']
    latest_amount = latest_breakfast['TRANAMT']
    latest_canteen = latest_breakfast['CANTEEN']

    # 返回结果
    breakfast_result = {
        "总次数": total_breakfast_count,
        "总金额": total_breakfast_amount,
        "常去的食堂": frequent_canteen,
        "常去食堂的次数": frequent_canteen_count,
        "常去食堂的总消费金额": frequent_canteen_amount,
        "常去的窗口": frequent_window,
        "常去窗口的次数": frequent_window_count,
        "常去窗口的总消费金额": frequent_window_amount,
        "最早吃早餐的时间": earliest_time,
        "最早吃早餐的金额": earliest_amount,
        "最早吃早餐的食堂": earliest_canteen,
        "最晚吃早餐的时间": latest_time,
        "最晚吃早餐的金额": latest_amount,
        "最晚吃早餐的食堂": latest_canteen
    }

    # 吃早餐总次数
    breakfast_count_int = breakfast_result["总次数"]
    breakfast_spent = breakfast_result["总金额"]

    # 吃早餐最常去的食堂
    breakfast_most_visited_canteen = breakfast_result["常去的食堂"]
    breakfast_most_visited_canteen_count = breakfast_result["常去食堂的次数"]
    breakfast_most_visited_canteen_spent = breakfast_result["常去食堂的总消费金额"]

    # 吃早餐最常去的窗口
    breakfast_most_visited_window = breakfast_result["常去的窗口"]
    breakfast_most_visited_window_count = breakfast_result["常去窗口的次数"]
    breakfast_most_visited_window_spent = breakfast_result["常去窗口的总消费金额"]

    # 吃早餐最早时间
    breakfast_earliest_time = breakfast_result["最早吃早餐的时间"]
    breakfast_earliest_time_cost = breakfast_result["最早吃早餐的金额"]
    breakfast_earliest_time_location = breakfast_result["最早吃早餐的食堂"]

    # 吃早餐最晚时间
    breakfast_latest_time = breakfast_result["最晚吃早餐的时间"]
    breakfast_latest_time_cost = breakfast_result["最晚吃早餐的金额"]
    breakfast_latest_time_location = breakfast_result["最晚吃早餐的食堂"]


    sub_title_2 = f"## 2.早餐\n"

    if breakfast_count_int < 100:
        sub_title_2_content_1 = f"""
{year}年，你在哈工小共吃了 **{breakfast_count_int}** 顿早餐，共花费 **{breakfast_spent:.2f}** 元。\n
生活虽忙，也要记得好好吃早餐！\n

"""
    elif breakfast_count_int == 0:
        sub_title_2_content_1 = f"""
{year}年，你在哈工小共吃了 **{breakfast_count_int}** 顿早餐，共花费 **{breakfast_spent:.2f}** 元。\n
从来不吃早餐？明年一定记得早点起床！\n

"""   
    else:
        sub_title_2_content_1 = f"""
{year}年，你在哈工小共吃了 **{breakfast_count_int}** 顿早餐，共花费 **{breakfast_spent:.2f}** 元。\n
早餐是一天中最重要的一餐，坚持吃早餐，保持不错继续坚持！\n

"""
    if breakfast_count_int > 1:
        sub_title_2_content_2 = f"""

还记得 **{breakfast_earliest_time}** 的时候，你在 **{breakfast_earliest_time_location}** 吃早餐，花了 **{breakfast_earliest_time_cost:.2f}** 元，这是你{year}年吃得最早的一餐；\n

当然，也别忘了 **{breakfast_latest_time}** 的时候，你在 **{breakfast_latest_time_location}** 吃早餐，花了 **{breakfast_latest_time_cost:.2f}** 元，虽然晚起了一会，但是也坚持去吃了早餐。\n

{year}年，你最喜欢去 **{breakfast_most_visited_canteen}** 吃早餐， 在这里吃了 **{breakfast_most_visited_canteen_count}** 顿早餐，共花费了 **{breakfast_most_visited_canteen_spent:.2f}** 元；\n
**{breakfast_most_visited_window}** 是你早餐的最爱，在这里点了 **{breakfast_most_visited_window_count}** 顿早餐，共花费了 **{breakfast_most_visited_window_spent:.2f}** 元。\n
"""
    # 午饭
    # 获取数据
    # 筛选出午饭时间段（11:00-13:59）
    df_lunch = df_filtered2[(df_filtered2['Hour'] >= 10) & (df_filtered2['Hour'] <= 13)]

    # 总次数和总金额
    total_lunch_count = len(df_lunch)
    total_lunch_amount = df_lunch['TRANAMT'].sum()

    # 常去的食堂（次数最多）
    frequent_canteen = df_lunch['CANTEEN'].value_counts().idxmax()
    frequent_canteen_count = df_lunch['CANTEEN'].value_counts().max()
    frequent_canteen_amount = df_lunch[df_lunch['CANTEEN'] == frequent_canteen]['TRANAMT'].sum()

    # 常去的窗口（次数最多）
    frequent_window = df_lunch['MERCNAME'].value_counts().idxmax()
    frequent_window_count = df_lunch['MERCNAME'].value_counts().max()
    frequent_window_amount = df_lunch[df_lunch['MERCNAME'] == frequent_window]['TRANAMT'].sum()

    # 最早吃午饭的记录
    df_lunch['Hour'] = df_lunch['OCCTIME'].dt.hour
    df_lunch['Adjusted_Hour'] = df_lunch['Hour'].apply(lambda x: x + 24 if x < 6 else x)

    earliest_lunch = df_lunch.loc[df_lunch['Adjusted_Hour'].idxmin()]
    earliest_time = earliest_lunch['OCCTIME']
    earliest_amount = earliest_lunch['TRANAMT']
    earliest_canteen = earliest_lunch['CANTEEN']

    # 最晚吃午饭的记录
    latest_lunch = df_lunch.loc[df_lunch['Adjusted_Hour'].idxmax()]
    latest_time = latest_lunch['OCCTIME']
    latest_amount = latest_lunch['TRANAMT']
    latest_canteen = latest_lunch['CANTEEN']

    # 返回结果
    lunch_result = {
            "总次数": total_lunch_count,
            "总金额": total_lunch_amount,
            "常去的食堂": frequent_canteen,
            "常去食堂的次数": frequent_canteen_count,
            "常去食堂的总消费金额": frequent_canteen_amount,
            "常去的窗口": frequent_window,
            "常去窗口的次数": frequent_window_count,
            "常去窗口的总消费金额": frequent_window_amount,
            "最早吃午饭的时间": earliest_time,
            "最早吃午饭的金额": earliest_amount,
            "最早吃午饭的食堂": earliest_canteen,
            "最晚吃午饭的时间": latest_time,
            "最晚吃午饭的金额": latest_amount,
            "最晚吃午饭的食堂": latest_canteen
    }
    # 吃午饭总次数
    lunch_count_int = lunch_result["总次数"]
    lunch_spent = lunch_result["总金额"]

    # 吃午饭最常去的食堂
    lunch_most_visited_canteen = lunch_result["常去的食堂"]
    lunch_most_visited_canteen_count = lunch_result["常去食堂的次数"]
    lunch_most_visited_canteen_spent = lunch_result["常去食堂的总消费金额"]

    # 吃午饭最常去的窗口
    lunch_most_visited_window = lunch_result["常去的窗口"]
    lunch_most_visited_window_count = lunch_result["常去窗口的次数"]
    lunch_most_visited_window_spent = lunch_result["常去窗口的总消费金额"]

    # 吃午饭最早时间
    lunch_earliest_time = lunch_result["最早吃午饭的时间"]
    lunch_earliest_time_cost = lunch_result["最早吃午饭的金额"]
    lunch_earliest_time_location = lunch_result["最早吃午饭的食堂"]

    # 吃午饭最晚时间
    lunch_latest_time = lunch_result["最晚吃午饭的时间"]
    lunch_latest_time_cost = lunch_result["最晚吃午饭的金额"]
    lunch_latest_time_location = lunch_result["最晚吃午饭的食堂"]

    sub_title_3 = f"## 3.午饭\n"
    sub_title_3_content = f"""
{year}年，你在哈工小共吃了 **{lunch_count_int}** 顿午饭，共花费 **{lunch_spent:.2f}** 元。\n
    
还记得 **{lunch_earliest_time}** 的时候就已经点好了 **{lunch_earliest_time_location}** ，这顿午饭花了 **{lunch_earliest_time_cost:.2f}** 元,这是你{year}年午餐吃得最早的一次；\n

另外，在 **{lunch_latest_time}** 的时候才去吃午饭，吃的是 **{lunch_latest_time_location}** ，花了 **{lunch_latest_time_cost:.2f}** 元，但你知道在哈工小，来晚了，就会没有什么东西可吃。\n

{year}年，你最喜欢去 **{lunch_most_visited_canteen}** 吃午饭， 在这里吃了 **{lunch_most_visited_canteen_count}** 顿午饭，共花费了 **{lunch_most_visited_canteen_spent:.2f}** 元；\n
**{lunch_most_visited_window}** 是你午餐的最爱，在这里点了 **{lunch_most_visited_window_count}** 顿午餐，共花费了 **{lunch_most_visited_window_spent:.2f}** 元。\n
    

"""

    # 晚饭

    # 获取数据
    df_dinner = df_filtered2[(df_filtered2['Hour'] >= 16) & (df_filtered2['Hour'] <= 19)]

    # 总次数和总金额
    total_dinner_count = len(df_dinner)
    total_dinner_amount = df_dinner['TRANAMT'].sum()

    # 常去的食堂（次数最多）
    frequent_canteen = df_dinner['CANTEEN'].value_counts().idxmax()
    frequent_canteen_count = df_dinner['CANTEEN'].value_counts().max()
    frequent_canteen_amount = df_dinner[df_dinner['CANTEEN'] == frequent_canteen]['TRANAMT'].sum()

    # 常去的窗口（次数最多）
    frequent_window = df_dinner['MERCNAME'].value_counts().idxmax()
    frequent_window_count = df_dinner['MERCNAME'].value_counts().max()
    frequent_window_amount = df_dinner[df_dinner['MERCNAME'] == frequent_window]['TRANAMT'].sum()

    # 最早吃晚饭的记录
    df_dinner['Hour'] = df_dinner['OCCTIME'].dt.hour
    df_dinner['Adjusted_Hour'] = df_dinner['Hour'].apply(lambda x: x + 24 if x < 6 else x)
    earliest_dinner = df_dinner.loc[df_dinner['Adjusted_Hour'].idxmin()]
    earliest_time = earliest_dinner['OCCTIME']
    earliest_amount = earliest_dinner['TRANAMT']
    earliest_canteen = earliest_dinner['CANTEEN']

    # 最晚吃晚饭的记录
    latest_dinner = df_dinner.loc[df_dinner['Adjusted_Hour'].idxmax()]
    latest_time = latest_dinner['OCCTIME']
    latest_amount = latest_dinner['TRANAMT']
    latest_canteen = latest_dinner['CANTEEN']

    # 返回结果
    dinner_result = {
        "总次数": total_dinner_count,
        "总金额": total_dinner_amount,
        "常去的食堂": frequent_canteen,
        "常去食堂的次数": frequent_canteen_count,
        "常去食堂的总消费金额": frequent_canteen_amount,
        "常去的窗口": frequent_window,
        "常去窗口的次数": frequent_window_count,
        "常去窗口的总消费金额": frequent_window_amount,
        "最早吃晚饭的时间": earliest_time,
        "最早吃晚饭的金额": earliest_amount,
        "最早吃晚饭的食堂": earliest_canteen,
        "最晚吃晚饭的时间": latest_time,
        "最晚吃晚饭的金额": latest_amount,
        "最晚吃晚饭的食堂": latest_canteen
    }
    # 吃晚饭总次数
    dinner_count_int = dinner_result["总次数"]
    dinner_spent = dinner_result["总金额"]

    # 吃晚饭最常去的食堂
    dinner_most_visited_canteen = dinner_result["常去的食堂"]
    dinner_most_visited_canteen_count = dinner_result["常去食堂的次数"]
    dinner_most_visited_canteen_spent = dinner_result["常去食堂的总消费金额"]

    # 吃晚饭最常去的窗口
    dinner_most_visited_window = dinner_result["常去的窗口"]
    dinner_most_visited_window_count = dinner_result["常去窗口的次数"]
    dinner_most_visited_window_spent = dinner_result["常去窗口的总消费金额"]

    # 吃晚饭最早时间
    dinner_earliest_time = dinner_result["最早吃晚饭的时间"]
    dinner_earliest_time_cost = dinner_result["最早吃晚饭的金额"]
    dinner_earliest_time_location = dinner_result["最早吃晚饭的食堂"]

    # 吃晚饭最晚时间
    dinner_latest_time = dinner_result["最晚吃晚饭的时间"]
    dinner_latest_time_cost = dinner_result["最晚吃晚饭的金额"]
    dinner_latest_time_location = dinner_result["最晚吃晚饭的食堂"]

    sub_title_4 = f"## 4.晚饭\n"

    sub_title_4_content = f"""
{year}年，你在哈工小共吃了 **{dinner_count_int}** 顿晚饭，共花费 **{dinner_spent:.2f}** 元。\n

**{dinner_earliest_time}** 就已经去点好了 **{dinner_earliest_time_location}** ，这顿晚饭花了 **{dinner_earliest_time_cost:.2f}** 元,这是你{year}年晚餐吃得最早的一次；\n

在 **{dinner_latest_time}** 的时候，已经快到宵夜时间你才去吃晚饭，吃的是 **{dinner_latest_time_location}** ，花了 **{dinner_latest_time_cost:.2f}** 元\n

{year}年，你最喜欢去 **{dinner_most_visited_canteen}** 吃晚饭，在这里吃了 **{dinner_most_visited_canteen_count}** 顿晚饭，共花费了 **{dinner_most_visited_canteen_spent:.2f}** 元；\n
**{dinner_most_visited_window}** 是你晚餐的最爱，在这里点了 **{dinner_most_visited_window_count}** 顿晚餐，共花费了 **{dinner_most_visited_window_spent:.2f}** 元。\n

"""
    
    # 宵夜
    sub_title_5 = f"## 5.宵夜\n"

    sub_title_5_content = f"""
{year}年，你在哈工小共吃了 **{0}** 顿宵夜，共花费 **{0}** 元。\n

因为，在哈工小，是没有宵夜提供的。
"""
    # 吃饭总览
    sub_title_6 = f"## 6.吃饭总览\n"

    sub_title_6_content = f"""
{year}年，你在哈工小共吃了 **{breakfast_count_int}** 顿早餐，共花费 **{breakfast_spent:.2f}** 元；\n
吃了 **{lunch_count_int}** 顿午饭，共花费 **{lunch_spent:.2f}** 元；\n
吃了 **{dinner_count_int}** 顿晚饭，共花费 **{dinner_spent:.2f}** 元。\n

一日三餐最爱去的食堂分别是 **{breakfast_most_visited_canteen}** 、 **{lunch_most_visited_canteen}** 、 **{dinner_most_visited_canteen}** ；\n

![图片]({result_path}2024年校园卡早餐午饭晚饭宵夜常去窗口次数排行.png) \n
![图片]({result_path}2024年校园卡早餐午饭晚饭宵夜常去食堂次数排行.png) \n

"""
    
    # 洗澡
    # 获取数据
    df_bath = df_data[df_data['MERCNAME'] == 'A17公寓浴池']

    # 按时间排序
    df_bath = df_bath.sort_values(by='OCCTIME').reset_index(drop=True)

    # 合并半小时内的消费为一次洗澡
    merged_bath_data = []
    start_time = None
    total_amount = 0

    for _, row in df_bath.iterrows():
        if start_time is None:
            # 初始化第一条记录
            start_time = row['OCCTIME']
            total_amount = row['TRANAMT']
        elif row['OCCTIME'] - start_time <= timedelta(minutes=30):
            # 如果在半小时内，累加金额
            total_amount += row['TRANAMT']
        else:
            # 如果超过半小时，记录前一次洗澡数据
            merged_bath_data.append({'Start_Time': start_time, 'Total_Amount': total_amount})
            # 初始化新的一次洗澡记录
            start_time = row['OCCTIME']
            total_amount = row['TRANAMT']

    # 添加最后一组洗澡数据
    if start_time is not None:
        merged_bath_data.append({'Start_Time': start_time, 'Total_Amount': total_amount})

    # 转换为DataFrame
    df_merged_bath = pd.DataFrame(merged_bath_data)
    df_merged_bath['Hour'] = df_merged_bath['Start_Time'].dt.hour
    df_merged_bath['Adjusted_Hour'] = df_merged_bath['Hour'].apply(lambda x: x + 24 if x < 6 else x)

    # 总次数和总金额
    total_bath_count = len(df_merged_bath)
    total_bath_amount = df_merged_bath['Total_Amount'].sum()

    # 最晚洗澡的记录
    latest_bath = df_merged_bath.iloc[df_merged_bath['Adjusted_Hour'].idxmax()]
    latest_time = latest_bath['Start_Time']
    latest_amount = latest_bath['Total_Amount']

    # 最常洗澡的时间
    frequent_hour = df_merged_bath['Hour'].mode()[0]  # 原始小时
    frequent_hour_data = df_merged_bath[df_merged_bath['Hour'] == frequent_hour]
    frequent_hour_amount = frequent_hour_data['Total_Amount'].sum()/len(frequent_hour_data)

    # 返回结果
    bath_result = {
        "洗澡总次数": total_bath_count,
        "洗澡总金额": total_bath_amount,
        "最晚洗澡时间": latest_time,
        "最晚洗澡金额": latest_amount,
        "最常洗澡的时间": f"{frequent_hour}:00",
        "最常洗澡时间的金额": frequent_hour_amount
    }

    # 洗澡总次数
    bath_count_int = bath_result["洗澡总次数"]
    bath_spent = bath_result["洗澡总金额"]

    # 洗澡最晚时间
    bath_latest_time = bath_result["最晚洗澡时间"]
    bath_latest_time_cost = bath_result["最晚洗澡金额"]
    bath_latest_time_location = "A17公寓"

    # 最常洗澡时间
    bath_most_time = bath_result["最常洗澡的时间"]
    bath_most_time_cost =  bath_result["最常洗澡时间的金额"]
    bath_most_time_location = "A17公寓"

    sub_title_7 = f"## 7.洗澡\n"

    sub_title_7_content = f"""
{year}年，你在哈工小共洗了 **{bath_count_int}** 次澡，共花费 **{bath_spent:.2f}** 元。\n

在 **{bath_latest_time}** 的时候，你才在 **{bath_latest_time_location}** 洗完澡，花费了 **{bath_latest_time_cost:.2f}** 元\n

{year}年，你最喜欢在 **{str(bath_most_time)}** 的时候去 **{bath_most_time_location}** 洗澡，在这个时间段里你一共花了 **{bath_most_time_cost:.2f}** 元\n

"""
    # 生成Markdown内容
    markdown_content = f"""
{tilte}

{sub_title_0}
{sub_title_0_content}

{sub_title_1}
{sub_title_1_content}

{sub_title_2}
{sub_title_2_content_1}

{sub_title_3}
{sub_title_3_content}

{sub_title_4}
{sub_title_4_content}

{sub_title_5}
{sub_title_5_content}

{sub_title_6}
{sub_title_6_content}

{sub_title_7}
{sub_title_7_content}

"""
    
with open(f'{username}_Annual_Summary_{year}.md', 'w', encoding='utf-8') as f:
    f.write(markdown_content)







