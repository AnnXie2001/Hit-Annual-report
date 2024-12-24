import os
import json
import config
from csv import DictWriter


def read_and_merge_json(folder_path):
    all_rows = []  # 用于存储合并后的所有行数据

    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder_path):
        # 判断文件是否为 JSON 格式
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)

            # 打开并读取 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    json_data = json.load(f)
                    if 'rows' in json_data:
                        all_rows.extend(json_data['rows'])  # 合并所有 rows
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from file {filename}: {e}")

    return all_rows

# 调用函数，指定文件夹路径
folder_path = './data'  # 请替换为你的文件夹路径
merged_data = read_and_merge_json(folder_path)

# 打印合并后的数据
print(merged_data)

# 获取json的键列表
fields = merged_data[0].keys()
# 用utf-8 +bom保存，可支持Excel查看
# newline要为空字符，因为csv模块有自己的新行管理办法
with open(config.output_file_name+'.csv', 'w', encoding='utf-8-sig',
          newline='') as f:
    writer = DictWriter(f, fieldnames=fields)
    # 写标题栏
    writer.writeheader()
    for rec in merged_data:
        # 这里获得的数据有末尾空格，去掉
        rec['MERCNAME'] = rec['MERCNAME'].strip()
        rec['TRANNAME'] = rec['TRANNAME'].strip()
        print(rec)
        writer.writerow(rec)