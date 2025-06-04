import pandas as pd

# Excel 文件路径（与脚本同层级）
files = {
    'April': '副本可力洛4月.xlsx',
    'March': '副本可力洛3月.xlsx',
    'February': '副本可力洛2月.xlsx',
    'January': '副本可力洛1月.xlsx'
}

# 读取每个月的数据
def read_excel_data(file_path):
    df = pd.read_excel(file_path, usecols=['就诊卡号', '医生'])
    df.columns = ['CardNumber', 'Doctor']
    return df

# 提取所有月份的数据
dataframes = {month: read_excel_data(path) for month, path in files.items()}

# 合并1-3月数据
all_previous = pd.concat([dataframes['January'], dataframes['February'], dataframes['March']])

# 获取4月新增数据
april_data = dataframes['April']
new_cards = april_data[~april_data['CardNumber'].isin(all_previous['CardNumber'])]

# 按医生分组输出
grouped_new_cards = new_cards.groupby('Doctor')['CardNumber'].apply(list).reset_index()

# 导出新增卡号明细
grouped_new_cards.to_excel('new_cards_april.xlsx', index=False, engine='openpyxl')

print('新增卡号明细已导出为 new_cards_april.xlsx')
