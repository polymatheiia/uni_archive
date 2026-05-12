import sys
import os
import pandas as pd
import plotly.graph_objects as go


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python plotly_data_stocks.py [0|1]")
        sys.exit(1)
    
    # Load stock data
    df = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)
    
    # Create figure
    fig = go.Figure()
    
    # Define colors for each stock
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Add trace for each stock
    for column, color in zip(df.columns, colors):
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            name=column,
            line=dict(color=color, width=2),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Date: %{x|%Y-%m-%d}<br>' +
                         'Price: $%{y:.2f}<br>' +
                         '<extra></extra>'
        ))
    
    # Update layout
    fig.update_layout(
        title={
            'text': 'Tech Stocks Price Movement (2023) - Click Legend to Toggle',
            'font': {'size': 16, 'weight': 'bold'}
        },
        xaxis_title='Date',
        yaxis_title='Stock Price ($)',
        hovermode='x unified',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            title="Stocks (Click to toggle)"
        ),
        width=1000,
        height=500,
        template='plotly_white'
    )
    
    # Enable legend click to toggle lines
    fig.update_layout(legend=dict(itemclick="toggle", itemdoubleclick="toggleothers"))
    
    # Handle output
    if sys.argv[1] == "0":
        fig.show()
    else:
        out_file = "plotly_data_stocks.html"
        fig.write_html(out_file)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
