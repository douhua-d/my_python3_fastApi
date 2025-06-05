import pandas as pd
import os

def analyze_and_export():
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 自动查找可力洛5月的Excel文件
    for fname in os.listdir(current_dir):
        if fname.startswith("可力洛5月") and fname.endswith(".xlsx"):
            excel_file = os.path.join(current_dir, fname)
            break
    else:
        print("未找到可力洛5月的Excel文件。")
        return

    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file)
        pills_per_box = 7

        # 新增一列"换算成盒数"
        def calc_boxes(row):
            if row['单位'] == '盒':
                return row['数量']
            elif row['单位'] == '片':
                return row['数量'] / pills_per_box
            else:
                return 0

        df['换算成盒数'] = df.apply(calc_boxes, axis=1)

        # 汇总统计
        total_boxes = df.loc[df['单位'] == '盒', '数量'].sum()
        total_pills = df.loc[df['单位'] == '片', '数量'].sum()
        pills_to_boxes = total_pills / pills_per_box if pills_per_box else 0
        total_boxes_all = total_boxes + pills_to_boxes

        summary = pd.DataFrame({
            '统计项': ['总销售盒数', '单位为片的总片数', '片数换算成盒数', '总盒数（含片数换算）'],
            '数值': [total_boxes, total_pills, round(pills_to_boxes, 2), round(total_boxes_all, 2)]
        })

        # 导出到新Excel，两个sheet
        output_path = os.path.join(current_dir, '可力洛5月_分析结果.xlsx')
        with pd.ExcelWriter(output_path) as writer:
            summary.to_excel(writer, sheet_name='汇总统计', index=False)
            df.to_excel(writer, sheet_name='明细数据', index=False)
        print(f"已导出新表格：{output_path}")

    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")

if __name__ == "__main__":
    analyze_and_export()
