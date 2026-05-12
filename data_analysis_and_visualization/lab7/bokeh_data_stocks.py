import sys
import os
import pandas as pd
from bokeh.plotting import figure, output_file, save, show
from bokeh.models import HoverTool
from bokeh.palettes import Category10_5


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python bokeh_data_stocks.py [0|1]")
        sys.exit(1)
    
    # Load stock data
    df = pd.read_csv('stock_data.csv', index_col='Date', parse_dates=True)
    
    # Create figure
    p = figure(
        title='Tech Stocks Price Movement',
        x_axis_type='datetime',
        x_axis_label='Date',
        y_axis_label='Stock Price ($)',
        width=1000,
        height=500,
        toolbar_location='above'
    )
    
    # Define colors
    colors = Category10_5
    
    # Add line for each stock
    for idx, column in enumerate(df.columns):
        line = p.line(
            df.index,
            df[column],
            legend_label=column,
            color=colors[idx],
            line_width=2,
            alpha=0.8,
            name=column
        )
    
    # Add hover tool
    hover = HoverTool(
        tooltips=[
            ('Stock', '$name'),
            ('Date', '@x{%F}'),
            ('Price', '$@y{0.00}')
        ],
        formatters={'@x': 'datetime'},
        mode='vline'
    )
    p.add_tools(hover)
    
    # Configure legend
    p.legend.location = "top_left"
    p.legend.title = "Stocks (Click to hide)"
    p.legend.click_policy = "hide"  # Click legend item to hide/show
    p.legend.background_fill_alpha = 0.8
    
    # Style the plot
    p.title.text_font_size = "14pt"
    p.title.text_font_style = "bold"
    p.grid.grid_line_alpha = 0.3
    
    # Handle output
    out_file = "bokeh_data_stocks.html"
    output_file(out_file)
    
    if sys.argv[1] == "0":
        show(p)
    else:
        save(p)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
