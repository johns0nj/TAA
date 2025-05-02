import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List
import numpy as np

def ask_for_filenames() -> List[str]:
    """
    询问用户要读取的Excel文件名列表
    
    Returns:
        List[str]: 用户输入的文件名列表
    """
    filenames = []
    while True:
        filename = input("请输入要读取的Excel文件名（输入'q'结束输入）：").strip()
        
        if filename.lower() == 'q':
            if not filenames:
                print("错误：至少需要输入一个文件名。")
                continue
            break
            
        # 检查文件是否存在
        if not os.path.exists(filename):
            print(f"错误：文件 '{filename}' 不存在，请重新输入。")
            continue
            
        # 检查文件扩展名
        if not filename.lower().endswith(('.xlsx', '.xls')):
            print("错误：请输入有效的Excel文件（.xlsx或.xls）。")
            continue
            
        filenames.append(filename)
        print(f"已添加文件：{filename}")
    
    return filenames

def read_time_series_excel(file_path: str, 
                          time_column: str = None,
                          date_format: str = None) -> pd.DataFrame:
    """
    从Excel文件读取时间序列数据
    
    Args:
        file_path: Excel文件路径
        time_column: 时间列的列名，如果为None则自动检测
        date_format: 时间格式（如'%Y-%m-%d'），如果为None则自动推断
        
    Returns:
        pd.DataFrame: 包含时间序列的数据框
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 如果未指定时间列，尝试自动检测
        if time_column is None:
            # 常见的时间列名
            possible_time_columns = ['Date', '时间', 'date', 'DATE', '日期', 'datetime', 'DateTime']
            for col in possible_time_columns:
                if col in df.columns:
                    time_column = col
                    break
            
            if time_column is None:
                raise ValueError("无法自动检测时间列，请手动指定时间列名")
        
        # 确保时间列存在
        if time_column not in df.columns:
            raise ValueError(f"找不到时间列 '{time_column}'")
        
        # 将时间列转换为datetime类型
        try:
            if date_format:
                df[time_column] = pd.to_datetime(df[time_column], format=date_format)
            else:
                # 尝试自动推断日期格式
                df[time_column] = pd.to_datetime(df[time_column], infer_datetime_format=True)
        except Exception as e:
            print(f"警告：日期转换时遇到问题，尝试使用混合格式：{e}")
            df[time_column] = pd.to_datetime(df[time_column], format='mixed')
        
        # 将时间列设置为索引
        df.set_index(time_column, inplace=True)
        
        # 按时间排序
        df.sort_index(inplace=True)
        
        print(f"\n文件 {os.path.basename(file_path)} 读取成功：")
        print(f"时间范围：{df.index.min()} 到 {df.index.max()}")
        print(f"数据列：{', '.join(df.columns)}")
        print("\n数据预览：")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"读取文件 {os.path.basename(file_path)} 时出错：{e}")
        return None

def read_multiple_excel_files(filenames: List[str], 
                            date_format: str = None) -> Dict[str, pd.DataFrame]:
    """
    读取多个Excel文件并返回数据框字典
    
    Args:
        filenames: Excel文件名列表
        date_format: 时间格式（如'%Y-%m-%d %H:%M:%S'）
        
    Returns:
        Dict[str, pd.DataFrame]: 文件名（不含扩展名）到数据框的映射
    """
    dataframes = {}
    
    for filename in filenames:
        # 获取文件名（不含扩展名）作为键
        key = os.path.splitext(os.path.basename(filename))[0]
        df = read_time_series_excel(filename, date_format=date_format)
        if df is not None:
            dataframes[key] = df
    
    return dataframes

def process_date_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    将日期格式处理为只精确到日
    
    Args:
        df: 输入的数据框
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    # 获取索引名称
    index_name = df.index.name
    
    # 将日期时间转换为只包含日期的格式
    df.index = pd.to_datetime(df.index).date
    
    # 恢复索引名称
    df.index.name = index_name
    
    return df

def add_holiday_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    在数据中插入假日数据，取值为最近一个交易日的值
    
    Args:
        df: 输入的数据框
        
    Returns:
        pd.DataFrame: 处理后的数据框
    """
    # 获取日期范围
    start_date = df.index.min()
    end_date = df.index.max()
    
    # 创建完整的日期范围（包括周末和假日）
    all_dates = pd.date_range(start=start_date, end=end_date, freq='D')
    all_dates = pd.to_datetime(all_dates).date
    
    # 创建新的数据框，包含所有日期
    new_df = pd.DataFrame(index=all_dates, columns=df.columns)
    
    # 使用前向填充方法填充缺失值（即使用最近一个交易日的值）
    new_df.update(df)
    new_df = new_df.fillna(method='ffill')
    
    return new_df

def process_dataframes(dataframes: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    处理所有数据框
    
    Args:
        dataframes: 输入的数据框字典
        
    Returns:
        Dict[str, pd.DataFrame]: 处理后的数据框字典
    """
    processed_dataframes = {}
    
    for name, df in dataframes.items():
        print(f"\n处理 {name} 数据...")
        
        # 处理日期格式
        df = process_date_format(df)
        print("  日期格式已处理为只精确到日")
        
        # 添加假日数据
        df = add_holiday_data(df)
        print("  已添加假日数据")
        
        processed_dataframes[name] = df
    
    return processed_dataframes

def save_dataframes_to_excel(dataframes: Dict[str, pd.DataFrame]) -> None:
    """
    将数据框保存到Excel文件
    
    Args:
        dataframes: 数据框字典，键为文件名，值为数据框
    """
    for name, df in dataframes.items():
        output_filename = f"{name}_df.xlsx"
        try:
            # 保存数据框到Excel文件
            df.to_excel(output_filename)
            print(f"成功保存 {name} 数据到文件：{output_filename}")
        except Exception as e:
            print(f"保存 {name} 数据时出错：{e}")

# 使用示例
if __name__ == "__main__":
    # 询问用户文件名列表
    filenames = ask_for_filenames()
    
    # 读取所有数据
    dataframes = read_multiple_excel_files(
        filenames=filenames,
        date_format=None  # 让程序自动推断日期格式
    )
    
    # 打印所有成功读取的数据框
    if dataframes:
        print("\n成功读取的数据框：")
        for name, df in dataframes.items():
            print(f"\n{name}:")
            print(f"  形状: {df.shape}")
            print(f"  列名: {', '.join(df.columns)}")
        
        # 处理数据框
        print("\n开始处理数据...")
        processed_dataframes = process_dataframes(dataframes)
        
        # 保存处理后的数据框到Excel文件
        print("\n正在保存处理后的数据框到Excel文件...")
        save_dataframes_to_excel(processed_dataframes)
