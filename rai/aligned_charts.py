import matplotlib.pyplot as plt
import pandas as pd
from excel_reader import read_multiple_excel_files, process_dataframes
import os
from typing import Dict

def plot_aligned_charts(dataframes: Dict[str, pd.DataFrame]) -> None:
    """
    绘制对齐的图表
    
    Args:
        dataframes: 数据框字典，键为文件名，值为数据框
    """
    # 获取数据框数量
    n_dataframes = len(dataframes)
    
    # 创建图形和子图
    fig, axes = plt.subplots(n_dataframes, 1, sharex=True, figsize=(12, 4*n_dataframes))
    
    # 如果只有一个数据框，将axes转换为列表
    if n_dataframes == 1:
        axes = [axes]
    
    # 为每个数据框创建图表
    for (name, df), ax in zip(dataframes.items(), axes):
        # 绘制所有列
        for column in df.columns:
            ax.plot(df.index, df[column], label=column)
        
        # 设置图表属性
        ax.set_title(name)
        ax.set_ylabel('Value')
        ax.legend()
        ax.grid(True)
    
    # 设置x轴标签（只在最后一个子图显示）
    axes[-1].set_xlabel('Date')
    
    # 调整子图之间的间距
    plt.subplots_adjust(hspace=0.3)
    
    # 自动调整日期标签的显示
    fig.autofmt_xdate()
    
    # 显示图表
    plt.show()

def main():
    # 获取当前目录下的所有_df.xlsx文件
    df_files = [f for f in os.listdir('.') if f.endswith('_df.xlsx')]
    
    if not df_files:
        print("未找到处理后的数据文件（*_df.xlsx）。请先运行excel_reader.py处理数据。")
        return
    
    # 读取所有处理后的数据文件
    dataframes = {}
    for file in df_files:
        name = file.replace('_df.xlsx', '')
        df = pd.read_excel(file, index_col=0)
        dataframes[name] = df
    
    # 绘制图表
    plot_aligned_charts(dataframes)

if __name__ == "__main__":
    main() 