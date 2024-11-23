import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Plotter:
    def __init__(self, data):
        """
        Initialize the Plotter class with a dataset.

        Args:
            data: Input data-frame containing variables to plot.
        """
        self.data = data

    def hist_plots(self, columns, rem_ol=False, thres=0.99, scale_graph=9, n_cols=3, aspect_ratio=2/3):
        """
        Create multiple histogram plots for specified columns.

        Args:
            columns: List of column names to plot.
            rem_ol: Remove observations greater than a specific percentile defined by `thres`.
            thres: Percentile used if `rem_ol=True`.
            scale_graph: Adjust the overall size of the graph.
            n_cols: Number of graphs per row.
            aspect_ratio: Aspect ratio of individual graphs.
        """
        n_rows = len(columns) // n_cols + (len(columns) % n_cols > 0)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(scale_graph, (scale_graph / n_cols) * aspect_ratio * n_rows))

        fig.suptitle(f'Histograms of {len(columns)} columns', y=1, size=15)
        axes = axes.flatten()

        for i, feature in enumerate(columns):
            if rem_ol:
                lim = self.data[feature].quantile([thres]).iloc[0]
                x = self.data[feature][self.data[feature] < lim]
                print(f'{feature}: Observations greater than P{round(thres * 100)} removed')
            else:
                x = self.data[feature]
            sns.histplot(data=x, ax=axes[i], kde=True)
        
        # Remove unused subplots
        for j in range(len(columns), len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()

    def violin_plots(self, outcome, x_columns, scale_graph=9, n_cols=3, aspect_ratio=2/3):
        """
        Create multiple violin plots by a categorical variable.

        Args:
            outcome: Categorical variable to use as hue.
            x_columns: List of column names to plot against `outcome`.
            scale_graph: Adjust the overall size of the graph.
            n_cols: Number of graphs per row.
            aspect_ratio: Aspect ratio of individual graphs.
        """
        n_rows = len(x_columns) // n_cols + (len(x_columns) % n_cols > 0)
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(scale_graph, (scale_graph / n_cols) * aspect_ratio * n_rows))

        fig.suptitle(f'Violin plots of {len(x_columns)} columns by {outcome}', y=1, size=15)
        axes = axes.flatten()

        for i, feature in enumerate(x_columns):
            sns.violinplot(data=self.data, ax=axes[i], y=feature, x=outcome)

        # Remove unused subplots
        for j in range(len(x_columns), len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()