# import pandas as pd
# import csv
#
# # 加载数据
# data = pd.read_csv('24S136027.csv')
#
# # 去除所有列的前后空格
# data = data.applymap(lambda x: str(x).strip() if isinstance(x, str) else x)
#
#
# # 定义分类函数
# def classify_place(merchant_name):
#     # 去除前后空格并转为小写
#     merchant_name = str(merchant_name)
#
#     if '紫丁香' in merchant_name:
#         return '学士负一楼'
#     elif any(keyword in merchant_name for keyword in ['友来', '回味斋', '民族']):
#         return '学士一楼'
#     elif '百味佳' in merchant_name:
#         return '学士二楼'
#     elif any(keyword in merchant_name for keyword in ['功夫厨房', '中央厨房']):
#         return '学苑负一楼'
#     elif any(keyword in merchant_name for keyword in ['学苑食堂', '学苑水果']):
#         return '学苑一楼'
#     elif any(keyword in merchant_name for keyword in ['川无界', '善谷', '小俄餐', '水果捞', '学苑二楼', '美食林']):
#         return '学苑一楼'
#     elif any(keyword in merchant_name for keyword in ['阳光广式猪脚饭', '小是小', '锦绣自选']):
#         return '学苑三楼'
#     elif '南苑' in merchant_name:
#         return '南苑食堂'
#     elif '丁香食堂' in merchant_name:
#         return '土木楼'
#     elif '西苑' in merchant_name:
#         return '西苑餐厅'
#     elif 'A17公寓' in merchant_name:
#         return 'A17公寓'
#     elif '校园车载' in merchant_name:
#         return '宝宝巴士'
#     elif '深澜网费' in merchant_name:
#         return '校园网'
#     else:
#         return '其他'
#
#
# # 为数据添加place列
# data['place'] = data['MERCNAME'].apply(classify_place)
#
# # 保存结果到新的CSV文件，使用标准的逗号分隔符，并处理可能的空格
# data.to_csv('Ann.csv', index=False, sep=',', quoting=csv.QUOTE_MINIMAL)
#
# # 输出前几行查看结果
# print(data.head())

import pandas as pd

# 读取CSV文件
df = pd.read_csv('Ann.csv')

# 定义分类函数
def categorize_canteen(row):
    if '学士' in row['PLACE']:
        return '学士食堂'
    elif '学苑' in row['PLACE']:
        return '学苑食堂'
    elif '南苑' in row['PLACE']:
        return '南苑食堂'
    elif '西苑' in row['PLACE']:
        return '西苑食堂'
    elif '丁香食堂' in row['PLACE']:
        return '土木楼'
    elif 'A17' in row['PLACE']:
        return 'A17公寓'
    elif '宝宝巴士' in row['PLACE']:
        return '宝宝巴士'
    else:
        return None

# 应用函数，新增CANTEEN列
df['CANTEEN'] = df.apply(categorize_canteen, axis=1)

# 将结果保存到新的CSV文件
df.to_csv('AnnNew.csv', index=False)

print("处理完成，数据已保存到 'AnnNew.csv'")
