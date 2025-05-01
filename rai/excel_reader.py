import pandas as pd
import os
from datetime import datetime

def ask_for_filename() -> str:
    """
    询问用户要读取的Excel文件名
    
    Returns:
        str: 用户输入的文件名
    """
    while True:
        filename = input("请输入要读取的Excel文件名（例如：data.xlsx）：").strip()
        
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"错误：文件 '{filename}' 不存在，请重新输入。")
            continue
            
        # 检查文件扩展名
        if not filename.lower().endswith(('.xlsx', '.xls')):
            print("错误：请输入有效的Excel文件（.xlsx或.xls）。")
            continue
            
        return filename

def read_time_series_excel(file_path: str, 
                          time_column: str = '时间',
                          date_format: str = None) -> pd.DataFrame:
    """
    从Excel文件读取时间序列数据
    
    Args:
        file_path: Excel文件路径
        time_column: 时间列的列名
        date_format: 时间格式（如'%Y-%m-%d %H:%M:%S'）
        
    Returns:
        pd.DataFrame: 包含时间序列的数据框
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 确保时间列存在
        if time_column not in df.columns:
            raise ValueError(f"找不到时间列 '{time_column}'")
        
        # 将时间列转换为datetime类型
        if date_format:
            df[time_column] = pd.to_datetime(df[time_column], format=date_format)
        else:
            df[time_column] = pd.to_datetime(df[time_column])
        
        # 将时间列设置为索引
        df.set_index(time_column, inplace=True)
        
        # 按时间排序
        df.sort_index(inplace=True)
        
        print("数据读取成功：")
        print(f"时间范围：{df.index.min()} 到 {df.index.max()}")
        print(f"数据列：{', '.join(df.columns)}")
        print("\n数据预览：")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 询问用户文件名
    file_path = ask_for_filename()
    
    # 读取数据
    df = read_time_series_excel(
        file_path=file_path,
        time_column='时间',  # 根据实际Excel文件中的列名修改
        date_format='%Y-%m-%d %H:%M:%S'  # 根据实际时间格式修改
    )
