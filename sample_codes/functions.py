import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def hist_plots(data, columns, rem_ol=False, thres=0.99, scale_graph=9, n_cols=3, aspect_ratio=2/3 ):
    '''Create multiple Histograms plots using a subset of variables specified.
    
    Args:
        data: Input data-frame containing variables we wish to plot.
        columns: Listing of column-names we wish to plot.
        rem_ol: Remove observations greater than specific percentile defined by thres argument.
        thres: Percentile that will be used if rem_ol=True.
        scale_graph: Adjust the total size of the graph.
        n_cols: Adjust how many graphs we have on each row.
        aspect_ratio: Adjust the aspect ratio of each individual graph. For squared graphs use 1/1.
    '''
    # Adjusting how many rows the grid will have and proper sizes
    n_rows = len(columns)//n_cols+(len(columns)%n_cols>0) 
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(scale_graph, (scale_graph/n_cols)*aspect_ratio*n_rows))

    # Plotting
    fig.suptitle(f'Histograms of {len(columns)} columns',y=1, size=15)
    axes=axes.flatten()
    for i,feature in enumerate(columns):
        if rem_ol:
            lim = data[feature].quantile([thres]).iloc[0]
            x = data[feature][data[feature]<lim]
            print(f'{feature}: Observations greater than P{round(thres*100)} removed')
        else:
            x=data[feature]
        sns.histplot(data=x,ax=axes[i], kde=True)
    plt.tight_layout()

def violin_plots(data, outcome, x_columns, scale_graph=9, n_cols=3, aspect_ratio=2/3 ):
    '''Create multiple violin plots by a categorical variable.
    
    Args:
        data: Input data-frame.
        outcome: Categorical variable that we will use as hue.
        x_columns: Listing of column-names we wish to plot against outcome.
        scale_graph: Adjust the total size of the graph.
        n_cols: Adjust how many graphs we have on each row.
        aspect_ratio: Adjust the aspect ratio of each individual graph. For squared graphs use 1/1.
    '''

    # Adjusting how many rows the grid will have and proper sizes
    n_rows = len(x_columns)//n_cols+(len(x_columns)%n_cols>0) 
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(scale_graph, (scale_graph/n_cols)*aspect_ratio*n_rows))

    # Plotting
    fig.suptitle(f'Violin plots of {len(x_columns)} columns by {outcome}',y=1, size=15)
    axes=axes.flatten()
    for i,feature in enumerate(x_columns):
        sns.violinplot(data=data, ax=axes[i],y=feature, x=outcome)
    plt.tight_layout()