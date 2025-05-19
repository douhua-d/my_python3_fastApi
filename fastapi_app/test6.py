import pandas as pd

# Excel 文件路径（与脚本同层级）
files = {
    'April': '可力洛4月.xlsx',
    'March': '可力洛3月.xlsx',
    'February': '可力洛2月.xlsx',
    'January': '可力洛1月.xlsx'
}

# 读取每个月的数据（包含所有列，而不仅仅是卡号和医生）
def read_excel_data(file_path):
    # 读取所有列，不再限制只读取就诊卡号和医生
    df = pd.read_excel(file_path)
    return df

# 提取所有月份的数据
dataframes = {month: read_excel_data(path) for month, path in files.items()}

# 从1-3月数据中提取出所有的就诊卡号（不需要其他信息）
previous_cards = set()
for month in ['January', 'February', 'March']:
    previous_cards.update(dataframes[month]['就诊卡号'].astype(str).tolist())

# 获取4月新增数据（完整的行，而不只是卡号）
april_data = dataframes['April']
# 将4月数据中就诊卡号不在之前月份的行筛选出来
new_cards_data = april_data[~april_data['就诊卡号'].astype(str).isin(previous_cards)]

# 按医生分组
grouped_new_cards = new_cards_data.groupby('医生')

# 创建一个ExcelWriter对象，用于将每个医生的数据写入不同的sheet
with pd.ExcelWriter('新增就诊卡号_4月.xlsx', engine='openpyxl') as writer:
    # 首先写入汇总sheet
    new_cards_data.to_excel(writer, sheet_name='全部新增', index=False)
    
    # 然后为每个医生创建单独的sheet
    for doctor, group in grouped_new_cards:
        # 使用医生名称作为sheet名
        sheet_name = f"{doctor}"[:31]  # Excel限制sheet名最长31字符
        group.to_excel(writer, sheet_name=sheet_name, index=False)

print('新增就诊卡号明细已导出为 新增就诊卡号_4月.xlsx')
