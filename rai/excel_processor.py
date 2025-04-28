import pandas as pd
from datetime import datetime
import os

def save_processed_excel(df: pd.DataFrame, 
                        original_filename: str,
                        process_type: str = 'processed',
                        output_dir: str = 'output') -> str:
    """
    保存处理后的Excel文件
    
    Args:
        df: 要保存的DataFrame
        original_filename: 原始文件名
        process_type: 处理类型，如'processed', 'formatted', 'cleaned'等
        output_dir: 输出目录
        
    Returns:
        str: 保存的文件路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取当前时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 从原始文件名中提取名称（不含扩展名）
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    
    # 构建新的文件名
    new_filename = f"{base_name}_{process_type}_{timestamp}.xlsx"
    
    # 完整的文件路径
    file_path = os.path.join(output_dir, new_filename)
    
    # 保存Excel文件
    df.to_excel(file_path, index=False)
    
    return file_path

def save_versioned_excel(df: pd.DataFrame,
                        original_filename: str,
                        version: int = 1,
                        output_dir: str = 'output') -> str:
    """
    保存带版本号的Excel文件
    
    Args:
        df: 要保存的DataFrame
        original_filename: 原始文件名
        version: 版本号
        output_dir: 输出目录
        
    Returns:
        str: 保存的文件路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 从原始文件名中提取名称（不含扩展名）
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    
    # 构建新的文件名
    new_filename = f"{base_name}_v{version}.xlsx"
    
    # 完整的文件路径
    file_path = os.path.join(output_dir, new_filename)
    
    # 保存Excel文件
    df.to_excel(file_path, index=False)
    
    return file_path

def save_analysis_excel(df: pd.DataFrame,
                       original_filename: str,
                       analysis_type: str,
                       output_dir: str = 'output') -> str:
    """
    保存分析结果Excel文件
    
    Args:
        df: 要保存的DataFrame
        original_filename: 原始文件名
        analysis_type: 分析类型，如'汇总', '统计', '分析'等
        output_dir: 输出目录
        
    Returns:
        str: 保存的文件路径
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 从原始文件名中提取名称（不含扩展名）
    base_name = os.path.splitext(os.path.basename(original_filename))[0]
    
    # 构建新的文件名
    new_filename = f"{base_name}_{analysis_type}.xlsx"
    
    # 完整的文件路径
    file_path = os.path.join(output_dir, new_filename)
    
    # 保存Excel文件
    df.to_excel(file_path, index=False)
    
    return file_path 