import pandas as pd
import os

def analyze_and_export():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_file = os.path.join(current_dir, "可力洛5月.xlsx")
    if not os.path.exists(excel_file):
        print("未找到可力洛5月.xlsx 文件。")
        return

    try:
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

        # 打印终端结果
        print("\n=== 可力洛5月销售数据分析 ===")
        print(f"总销售盒数: {total_boxes} 盒")
        print(f"单位为片的总片数: {total_pills} 片")
        print(f"片数换算成盒数: {pills_to_boxes:.2f} 盒")
        print(f"总盒数（含片数换算）: {total_boxes_all:.2f} 盒")

        # 汇总表
        summary = pd.DataFrame({
            '统计项': ['总销售盒数', '单位为片的总片数', '片数换算成盒数', '总盒数（含片数换算）'],
            '数值': [total_boxes, total_pills, round(pills_to_boxes, 2), round(total_boxes_all, 2)]
        })

        # 导出到新Excel，两个sheet
        output_path = os.path.join(current_dir, '5月可力洛销售数据分析报告.xlsx')
        with pd.ExcelWriter(output_path) as writer:
            summary.to_excel(writer, sheet_name='汇总统计', index=False)
            df.to_excel(writer, sheet_name='明细数据', index=False)
        print(f"\n已导出新表格：{output_path}")

    except Exception as e:
        print(f"分析过程中出现错误: {str(e)}")

if __name__ == "__main__":
    analyze_and_export()
