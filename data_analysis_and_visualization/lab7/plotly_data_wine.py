import sys
import os
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_wine


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["0", "1"]:
        print("Usage: python plotly_data_wine.py [0|1]")
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
    colors = ['red', 'green', 'blue']
    color_map = [colors[target] for target in y]

    # Create subplot grid
    fig = make_subplots(
        rows=4, cols=4,
        shared_xaxes='columns',
        shared_yaxes='rows',
        vertical_spacing=0.02,
        horizontal_spacing=0.02
    )

    # Create scatter plots
    for i in range(4):
        for j in range(4):
            row = 4 - i  # Reverse row order to match mpld3 layout
            col = j + 1

            if i == j:
                # Diagonal: add feature name as annotation
                fig.add_annotation(
                    text=selected_features[i],
                    xref=f"x{(row - 1) * 4 + col}",
                    yref=f"y{(row - 1) * 4 + col}",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(size=12),
                    xanchor='center',
                    yanchor='middle'
                )

            # Add scatter plot for each class separately for legend
            for class_idx, class_name in enumerate(target_names):
                mask = y == class_idx

                fig.add_trace(
                    go.Scattergl(
                        x=X[mask, feature_idx[j]],
                        y=X[mask, feature_idx[i]],
                        mode='markers',
                        marker=dict(
                            color=colors[class_idx],
                            size=6,
                            opacity=0.6
                        ),
                        name=class_name,
                        legendgroup=class_name,
                        showlegend=(i == 0 and j == 0),  # Show legend only once
                        hovertemplate=f'{selected_features[j]}: %{{x:.2f}}<br>' +
                                      f'{selected_features[i]}: %{{y:.2f}}<br>' +
                                      f'Class: {class_name}<extra></extra>'
                    ),
                    row=row,
                    col=col
                )

    # Update layout
    fig.update_layout(
        title="Wine Dataset - Interactive Scatter Matrix with Linked Brushing",
        height=800,
        width=800,
        hovermode='closest',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    # Remove axis labels except for outer edges
    for i in range(1, 17):
        fig.update_xaxes(showticklabels=False, row=(i - 1) // 4 + 1, col=(i - 1) % 4 + 1)
        fig.update_yaxes(showticklabels=False, row=(i - 1) // 4 + 1, col=(i - 1) % 4 + 1)

    # Add axis labels on outer edges
    for j in range(4):
        fig.update_xaxes(
            title_text=selected_features[j],
            showticklabels=True,
            row=4,
            col=j + 1
        )

    for i in range(4):
        fig.update_yaxes(
            title_text=selected_features[i],
            showticklabels=True,
            row=4 - i,
            col=1
        )

    # Handle output
    if sys.argv[1] == "0":
        fig.show()
    else:
        out_file = "plotly_data_wine.html"
        fig.write_html(out_file)
        print(os.path.abspath(out_file))


if __name__ == "__main__":
    main()
