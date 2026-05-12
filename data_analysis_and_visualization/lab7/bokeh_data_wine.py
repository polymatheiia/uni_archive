import sys
import os
import numpy as np
from bokeh.plotting import figure, output_file, save, show
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Category10_3
from sklearn.datasets import load_wine


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python bokeh_data_wine.py [0|1]")
        sys.exit(1)

    # Load wine dataset
    wine = load_wine()
    X = wine.data
    y = wine.target
    feature_names = wine.feature_names
    target_names = wine.target_names

    # Add small random noise to avoid overlapping points
    X = X + 0.1 * np.random.random(X.shape)

    # Select 4 features for a 4x4 scatter matrix
    feature_idx = [0, 1, 5, 6]
    # 0 = alcohol
    # 1 = malic_acid
    # 5 = flavanoids
    # 6 = nonflavanoid_phenols

    selected_features = [feature_names[i] for i in feature_idx]

    # Create color map for classes
    colors = Category10_3
    color_list = [colors[target] for target in y]

    # Prepare data dictionary for ColumnDataSource
    data_dict = {
        'color': color_list,
        'class': [target_names[t] for t in y]
    }

    for idx, feat_idx in enumerate(feature_idx):
        data_dict[selected_features[idx]] = X[:, feat_idx]

    # Create shared ColumnDataSource for linked brushing
    source = ColumnDataSource(data=data_dict)

    # Create figure grid
    plots = []

    for i in range(4):
        row_plots = []
        for j in range(4):
            # Create tools
            tools = "pan,wheel_zoom,box_select,lasso_select,reset"

            # Create figure
            p = figure(
                width=200,
                height=200,
                tools=tools,
                toolbar_location=None,
                title=None
            )

            if i == j:
                # Diagonal: show feature name
                p.text(
                    x=[0.5],
                    y=[0.5],
                    text=[selected_features[i]],
                    text_align="center",
                    text_baseline="middle",
                    text_font_size="10pt"
                )
                p.axis.visible = False
                p.grid.visible = False
            else:
                # Off-diagonal: scatter plot
                p.scatter(
                    x=selected_features[j],
                    y=selected_features[i],
                    source=source,
                    size=6,
                    color='color',
                    alpha=0.6,
                    selection_color="color",
                    nonselection_fill_alpha=0.2,
                    nonselection_fill_color="color",
                    nonselection_line_alpha=0.2
                )

                # Add hover tool
                hover = HoverTool(
                    tooltips=[
                        (selected_features[j], f'@{{{selected_features[j]}}}{{0.00}}'),
                        (selected_features[i], f'@{{{selected_features[i]}}}{{0.00}}'),
                        ('Class', '@class')
                    ]
                )
                p.add_tools(hover)

            # Remove tick labels except for outer edges
            if i < 3:  # Not bottom row
                p.xaxis.major_label_text_font_size = '0pt'
            else:
                p.xaxis.axis_label = selected_features[j]
                p.xaxis.axis_label_text_font_size = '8pt'

            if j > 0:  # Not left column
                p.yaxis.major_label_text_font_size = '0pt'
            else:
                p.yaxis.axis_label = selected_features[i]
                p.yaxis.axis_label_text_font_size = '8pt'

            row_plots.append(p)

        plots.append(row_plots)

    # Reverse rows to match mpld3 layout (bottom to top)
    plots = plots[::-1]

    # Create grid layout
    grid = gridplot(plots, toolbar_location='right')

    # Handle output
    out_file = "bokeh_data_wine.html"
    output_file(out_file)

    if sys.argv[1] == "0":
        show(grid)
    else:
        save(grid)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
