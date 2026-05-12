import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python mpld3_data_stocks.py [0|1]")
        sys.exit(1)
    
    # Load stock data
    df = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Define colors for each stock
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    # Plot each stock
    lines = []
    labels = []
    for idx, (column, color) in enumerate(zip(df.columns, colors)):
        line, = ax.plot(df.index, df[column], 
                       label=column, 
                       color=color, 
                       linewidth=2,
                       alpha=0.8)
        lines.append(line)
        labels.append(column)
    
    # Set labels and title
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Stock Price ($)', fontsize=12)
    ax.set_title('Tech Stocks Price Movement (2023) - Click Legend to Toggle', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    fig.autofmt_xdate()
    
    # Add interactive legend
    interactive_legend = plugins.InteractiveLegendPlugin(lines, labels, alpha_unsel=0.1)
    plugins.connect(fig, interactive_legend)
    
    # Handle output
    if sys.argv[1] == "0":
        mpld3.show()
    else:
        out_file = "mpld3_data_stocks.html"
        mpld3.save_html(fig, out_file)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
