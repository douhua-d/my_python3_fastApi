import pandas as pd
import os

def analyze_monthly_sales():
    """分析4-10月的可力洛销售数据，统一转换为盒数进行对比"""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pills_per_box = 7  # 每盒7片
    
    # 定义文件路径
    files = {
        '4月': '可力洛4月.xlsx',
        '5月': '可力洛5月.xlsx',
        '6月': '可力洛6月.xlsx', 
        '7月': '可力洛7月.xlsx',
        '8月': '可力洛8月.xlsx',
        '9月': '可力洛9月.xlsx',
        '10月': '可力洛10月.xlsx'
    }
    
    monthly_stats = []
    
    print("=== 可力洛4-10月销售数据对比分析 ===\n")
    
    for month, filename in files.items():
        file_path = os.path.join(current_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"警告: 未找到 {filename} 文件，跳过{month}数据")
            continue
            
        try:
            # 读取Excel数据
            df = pd.read_excel(file_path)
            
            if df.empty:
                print(f"警告: {filename} 文件为空，跳过{month}数据")
                continue
            
            # 统计盒数和片数
            total_boxes = df.loc[df['单位'] == '盒', '数量'].sum() if '盒' in df['单位'].values else 0
            total_pills = df.loc[df['单位'] == '片', '数量'].sum() if '片' in df['单位'].values else 0
            
            # 片数转换为盒数
            pills_to_boxes = total_pills / pills_per_box if total_pills > 0 else 0
            
            # 总盒数（含片数转换）
            total_boxes_all = total_boxes + pills_to_boxes
            
            # 统计记录数（销售条目数）
            total_records = len(df)
            
            # 统计就诊卡号数量
            unique_cards = df['就诊卡号'].nunique() if '就诊卡号' in df.columns else 0
            
            # 统计医生数量
            unique_doctors = df['医生'].nunique() if '医生' in df.columns else 0
            
            # 打印当月统计
            print(f"--- {month}销售数据 ---")
            print(f"销售盒数: {total_boxes} 盒")
            print(f"销售片数: {total_pills} 片")
            print(f"片数换算成盒数: {pills_to_boxes:.2f} 盒")
            print(f"总盒数（含片数换算）: {total_boxes_all:.2f} 盒")
            print(f"销售条目数: {total_records}")
            print(f"就诊卡号数: {unique_cards}")
            print(f"医生数: {unique_doctors}")
            print()
            
            # 保存统计数据
            monthly_stats.append({
                '月份': month,
                '销售盒数': total_boxes,
                '销售片数': total_pills,
                '片数换算成盒数': round(pills_to_boxes, 2),
                '总盒数（含片数换算）': round(total_boxes_all, 2),
                '销售条目数': total_records,
                '就诊卡号数': unique_cards,
                '医生数': unique_doctors
            })
            
        except Exception as e:
            print(f"读取 {filename} 时出现错误: {str(e)}")
            continue
    
    if not monthly_stats:
        print("没有成功读取任何月份的数据")
        return
    
    # 创建汇总DataFrame
    summary_df = pd.DataFrame(monthly_stats)
    
    # 按月份排序
    month_order = ['4月', '5月', '6月', '7月', '8月', '9月', '10月']
    summary_df['月份'] = pd.Categorical(summary_df['月份'], categories=month_order, ordered=True)
    summary_df = summary_df.sort_values('月份')
    
    print("=== 月度对比汇总表 ===")
    print(summary_df.to_string(index=False))
    print()
    
    # 计算环比增长率
    if len(summary_df) > 1:
        print("=== 环比增长分析（总盒数） ===")
        for i in range(1, len(summary_df)):
            current_month = summary_df.iloc[i]['月份']
            prev_month = summary_df.iloc[i-1]['月份']
            current_boxes = summary_df.iloc[i]['总盒数（含片数换算）']
            prev_boxes = summary_df.iloc[i-1]['总盒数（含片数换算）']
            
            if prev_boxes > 0:
                growth_rate = ((current_boxes - prev_boxes) / prev_boxes) * 100
                print(f"{current_month}相比{prev_month}: {growth_rate:+.2f}%")
            else:
                print(f"{current_month}相比{prev_month}: 无法计算（前月为0）")
        print()
    
    # 导出到Excel
    try:
        output_path = os.path.join(current_dir, '4-10月销售数据对比分析报告.xlsx')
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 汇总统计表
            summary_df.to_excel(writer, sheet_name='月度对比汇总', index=False)
            
            # 各月详细数据（如果需要的话）
            for month, filename in files.items():
                file_path = os.path.join(current_dir, filename)
                if os.path.exists(file_path):
                    try:
                        df = pd.read_excel(file_path)
                        if not df.empty:
                            # 添加换算成盒数列
                            def calc_boxes(row):
                                if row['单位'] == '盒':
                                    return row['数量']
                                elif row['单位'] == '片':
                                    return row['数量'] / pills_per_box
                                else:
                                    return 0
                            
                            df['换算成盒数'] = df.apply(calc_boxes, axis=1)
                            df.to_excel(writer, sheet_name=f'{month}详细数据', index=False)
                    except Exception as e:
                        print(f"导出{month}详细数据时出错: {str(e)}")
        
        print(f"分析报告已导出到: {output_path}")
        
    except Exception as e:
        print(f"导出Excel文件时出现错误: {str(e)}")

if __name__ == "__main__":
    analyze_monthly_sales()
