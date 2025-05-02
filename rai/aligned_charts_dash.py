import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import pandas as pd
import os
from typing import Dict

def create_aligned_charts(dataframes: Dict[str, pd.DataFrame]) -> go.Figure:
    """
    创建对齐的图表
    
    Args:
        dataframes: 数据框字典，键为文件名，值为数据框
    
    Returns:
        go.Figure: 包含所有子图的单个图表
    """
    # 获取数据框数量
    n_dataframes = len(dataframes)
    
    # 创建子图
    fig = make_subplots(
        rows=n_dataframes,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=list(dataframes.keys())
    )
    
    # 为每个数据框创建子图
    for i, (name, df) in enumerate(dataframes.items(), 1):
        # 为每个列添加轨迹
        for column in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    name=f"{name} - {column}",
                    mode='lines'
                ),
                row=i,
                col=1
            )
    
    # 设置布局
    fig.update_layout(
        title="对齐图表展示",
        height=400 * n_dataframes,
        showlegend=True,
        margin=dict(l=40, r=40, t=40, b=40),
        # 添加十字线配置
        hovermode='x unified',
        spikedistance=1000,
        hoverdistance=100
    )
    
    # 为每个子图设置y轴标题和类型
    for i, name in enumerate(dataframes.keys(), 1):
        if 'spx' in name.lower():
            fig.update_yaxes(
                title_text="Value (Log Scale)",
                type="log",
                row=i,
                col=1,
                # 添加十字线配置
                showspikes=True,
                spikemode='across+marker',
                spikesnap='cursor',
                spikecolor='black',
                spikethickness=1,
                spikedash='dot'
            )
        else:
            fig.update_yaxes(
                title_text="Value",
                row=i,
                col=1,
                # 添加十字线配置
                showspikes=True,
                spikemode='across+marker',
                spikesnap='cursor',
                spikecolor='black',
                spikethickness=1,
                spikedash='dot'
            )
    
    # 设置x轴
    fig.update_xaxes(
        rangeslider=dict(visible=True),
        type='date',
        row=n_dataframes,
        col=1,
        # 添加十字线配置
        showspikes=True,
        spikemode='across+marker',
        spikesnap='cursor',
        spikecolor='black',
        spikethickness=1,
        spikedash='dot'
    )
    
    # 为每个子图添加x轴十字线
    for i in range(1, n_dataframes):
        fig.update_xaxes(
            showspikes=True,
            spikemode='across+marker',
            spikesnap='cursor',
            spikecolor='black',
            spikethickness=1,
            spikedash='dot',
            row=i,
            col=1
        )
    
    return fig

# 初始化Dash应用
app = dash.Dash(__name__)

# 定义应用布局
app.layout = html.Div([
    html.H1('对齐图表展示'),
    dcc.Graph(
        id='aligned-charts',
        config={'scrollZoom': True}
    )
])

@app.callback(
    Output('aligned-charts', 'figure'),
    Input('aligned-charts', 'relayoutData')
)
def update_charts(relayout_data):
    # 获取当前目录下的所有_df.xlsx文件
    df_files = [f for f in os.listdir('.') if f.endswith('_df.xlsx')]
    
    if not df_files:
        return go.Figure()
    
    # 读取所有处理后的数据文件
    dataframes = {}
    for file in df_files:
        name = file.replace('_df.xlsx', '')
        df = pd.read_excel(file, index_col=0)
        dataframes[name] = df
    
    # 创建图表
    fig = create_aligned_charts(dataframes)
    
    # 如果存在缩放数据，应用缩放
    if relayout_data and 'xaxis.range[0]' in relayout_data:
        fig.update_xaxes(range=[relayout_data['xaxis.range[0]'], relayout_data['xaxis.range[1]']])
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True) 