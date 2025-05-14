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
    
    # 获取RAI momentum和headline的最新值
    latest_values = {}
    latest_date = None
    spx_latest = None
    spx_date = None
    
    for name, df in dataframes.items():
        if 'RAI' in name.upper():
            latest_date = df.index[-1].strftime('%Y-%m-%d')
            for column in df.columns:
                if 'momentum' in column.lower() or 'headline' in column.lower():
                    latest_value = df[column].iloc[-1]
                    latest_values[f"{name}_{column}"] = latest_value
        elif 'SPX' in name.upper():
            spx_date = df.index[-1].strftime('%Y-%m-%d')
            spx_latest = df.iloc[-1, 0]  # 获取第一列的最新值
    
    # 创建子图标题
    subplot_titles = []
    for name in dataframes.keys():
        title = name
        if 'RAI' in name.upper():
            title += f" (最新日期: {latest_date})"
            for col in dataframes[name].columns:
                if 'momentum' in col.lower() or 'headline' in col.lower():
                    key = f"{name}_{col}"
                    if key in latest_values:
                        title += f" ({col}: {latest_values[key]:.2f})"
        elif 'SPX' in name.upper():
            title += f" (最新日期: {spx_date}, 最新值: {spx_latest:.2f})"
        subplot_titles.append(title)
    
    # 创建子图
    fig = make_subplots(
        rows=n_dataframes,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=subplot_titles
    )
    
    # 计算SPX的3个月收益率
    spx_data = None
    for name, df in dataframes.items():
        if 'SPX' in name.upper():
            spx_data = df.iloc[:, 0]  # 获取第一列数据
            break
    
    if spx_data is not None:
        # 计算3个月收益率
        spx_returns = spx_data.pct_change(periods=63)  # 约3个月（21个交易日/月）
        # 找出下跌超过10%的时期
        crash_periods = spx_returns[spx_returns < -0.1]
        
        # 为每个子图添加阴影
        for i in range(1, n_dataframes + 1):
            for date in crash_periods.index:
                # 确保日期是datetime类型
                start_date = pd.to_datetime(date)
                end_date = start_date + pd.Timedelta(days=63)
                
                fig.add_vrect(
                    x0=start_date,
                    x1=end_date,
                    fillcolor="rgba(255, 165, 0, 0.2)",  # 浅橙色，透明度0.2
                    layer="below",
                    line_width=0,
                    row=i,
                    col=1
                )
    
    # 为每个数据框创建子图
    for i, (name, df) in enumerate(dataframes.items(), 1):
        # 为每个列添加轨迹
        for column in df.columns:
            # 设置SPX线的颜色为绿色
            line_color = 'green' if 'SPX' in name.upper() else None
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df[column],
                    name=f"{name} - {column}",
                    mode='lines',
                    line=dict(color=line_color) if line_color else None
                ),
                row=i,
                col=1
            )
            
            # 如果是RAI headline数据，添加均线
            if 'RAI' in name.upper() and 'headline' in column.lower():
                # 添加0均线
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=[0] * len(df),
                        name='0均线',
                        mode='lines',
                        line=dict(dash='dot', color='gray', width=1),
                        showlegend=False
                    ),
                    row=i,
                    col=1
                )
                
                # 添加±1均线
                for value in [-1, 1]:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=[value] * len(df),
                            name=f'{value}均线',
                            mode='lines',
                            line=dict(dash='dot', color='green', width=0.8),
                            showlegend=False
                        ),
                        row=i,
                        col=1
                    )
                
                # 添加±2均线
                for value in [-2, 2]:
                    fig.add_trace(
                        go.Scatter(
                            x=df.index,
                            y=[value] * len(df),
                            name=f'{value}均线',
                            mode='lines',
                            line=dict(dash='dot', color='blue', width=0.8),
                            showlegend=False
                        ),
                        row=i,
                        col=1
                    )
    
    # 设置布局
    fig.update_layout(
        title="GS Risk Appetite Index vs 标普500指数对比",
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
        if 'SPX' in name.upper():
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
    html.H1('GS Risk Appetite Index vs 标普500指数对比'),
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