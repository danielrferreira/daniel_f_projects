import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.stats import chi2_contingency
import numpy as np
from sklearn.ensemble import RandomForestClassifier

sns.set_theme(style="darkgrid", palette="deep")

class eda_aid:
    def __init__(self, df: pd.DataFrame):
        """ 
        Initialize the problem

        Args:
            df: DataFrame to be analyzed
        """
        self.df = df
        self.n_rows = self.df.shape[0]
        self.n_cols = self.df.shape[1]
        self.numeric_list = list(self.df.select_dtypes(include=['number']).columns)
        self.categorical_list = list(self.df.select_dtypes(include=['object']).columns)
        self.boolean_list = list(self.df.select_dtypes(include=['bool']).columns)
        self.missing_list = self.df.columns[self.df.isna().any()].tolist()
        self.non_missing_list = list(set(self.df.columns) - set(self.missing_list))
        print(f"EDA Aid initialized with {self.n_rows} rows and {self.n_cols} columns:\n - Numeric: {len(self.numeric_list)}\n - Object: {len(self.categorical_list)}\n - Boolean: {len(self.boolean_list)}")

    def missingness(self) -> pd.DataFrame:
        """
        Calculate the count and proportion of missing values in each column of the DataFrame.

        Returns:
            pd.DataFrame: A DataFrame with the count and proportion of missing values for each column.
        """
        missing_count = self.df.isna().sum()
        missings = pd.DataFrame({
            'missing_count': missing_count,
            'missing_proportions': round(missing_count / len(self.df),3)
        })
        return missings
    
    def columns_df(self) -> pd.DataFrame:
        """
        Create a DataFrame with column names, their types (numeric or object), and missing values information.

        Returns:
            pd.DataFrame: DataFrame with columns - 'name', 'type', 'count', and 'proportions'.
        """
        columns = self.numeric_list + self.categorical_list + self.boolean_list
        types = ['numeric'] * len(self.numeric_list) + ['object'] * len(self.categorical_list) + ['boolean'] * len(self.boolean_list)
        df_columns = pd.DataFrame({'name': columns, 'type': types})
        missings = self.missingness().reset_index().rename(columns={'index': 'name'})
        merged_df = pd.merge(df_columns, missings, on='name', how='left')
        merged_df.set_index('name', inplace=True)
        merged_df['non_missing_count'] = self.n_rows - merged_df['missing_count']
        return merged_df
    
    def missingness_chi_whitin(self) -> None:
        """
        This function shows the p-value of chi-square test of all columns with missing value. 0 means percfect association. 
        Larger values means independence of missingness.
        """
        p_values = pd.DataFrame(index = self.missing_list, columns=self.missing_list)
        for col1 in self.missing_list:
            for col2 in self.missing_list:
                if col1 == col2:
                    p_values.loc[col1, col2] = 0
                else:
                    contingency_table = pd.crosstab(self.df[col1].isna(), self.df[col2].isna())
                    _, p, _, _ = chi2_contingency(contingency_table)
                    p_values.loc[col1, col2] = p
        plt.figure(figsize=(8, 6))
        sns.heatmap(round(p_values.astype(float),5), annot=True, cmap='coolwarm_r', cbar_kws={'label': 'p-value'}, annot_kws={"size": 10})
        plt.title(f'Chi-Square Test p-value for Missing Values Associations')
        plt.show()
    
    def random_forest_importance(self, outcome, inputs, ax=None) -> plt.Axes:
        """ 
        Creates a bar plot of variable importance to predict an outcome.
        
        Args:
        outcome (pd.Series): Outcome variable (binary).
        inputs (list): List of input column names to be used.
        ax (plt.Axes, optional): Axis to draw the plot. Creates a new one if not provided.
        
        Returns:
        plt.Axes: Axis object containing the bar plot.
        """
        X = self.df[inputs]
        X = pd.get_dummies(X, drop_first=True)
        rank_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rank_model.fit(X, outcome)
        feature_importances = pd.Series(rank_model.feature_importances_, index=rank_model.feature_names_in_)
        feature_importances = feature_importances.sort_values()
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, len(feature_importances) * 0.3))
        ax.barh(feature_importances.index, feature_importances)
        ax.set_title("Feature Importance")
        ax.set_xlabel("Importance Score")
        ax.set_ylabel("Features")
        return ax
    
    def missingness_association(self, inputs=None, max_c=50):
        """ 
        Get all bar plots of variable importance to predict missingness.
        
        Args:
            inputs (list): List of input column names to be used. If None, all non missing numeric, boolean or object with low cardinality will be used.
            max_c: maximun value of unique categories in object variable
        
        """
        if inputs is None:
            inputs = [
                var for var in self.non_missing_list
                if pd.api.types.is_numeric_dtype(self.df[var])
                or (pd.api.types.is_object_dtype(self.df[var]) and self.df[var].nunique() < max_c)
                or pd.api.types.is_bool_dtype(self.df[var])
            ]
        n_graphs = len(self.missing_list)
        n_rows = math.ceil(n_graphs / 2)
        fig, axes = plt.subplots(nrows=n_rows, ncols=2, figsize=(12, n_rows * 6.6))
        axes = axes.flatten()
        fig.suptitle('Missigness Association', fontsize=20, y=1.0025)
        for var, ax in zip(self.missing_list, axes):
            outcome = self.df[var].isna()
            self.random_forest_importance(outcome, inputs, ax=ax)
            ax.set_title(var)
        for ax in axes[n_graphs:]:
            ax.axis("off")
        plt.tight_layout()
        plt.show()

    def ln_analysis(self, outcome, x_columns = None, bins = 10, rem_ol = False, thres_1 = 0.05, thres_2 = 0.95):
        '''
        This function helps understand if polynomial terms and/or transformations are needed in a logistic regression. It calculates ln(p/(1-p)) of each bin of numerical columns.
        It also plot the ranges used, and a kernel distribution to help decide which transformation or polynomial term would help.
        If the relationship looks like linear, no need of polynomial term.
        Args:
            outcome: Categorical variable that we will use to calculate ln(p/(1-p)).
            x_columns: Listing of column-names we wish to plot against outcome.
            bins: How many bins we will use to cut the numerical x column
            rem_ol: Remove anything lower than thres_1 percentile or higher than thres_2 percentile
            thres_1: Lower Percentile 
            thres_2: Higher Percentile 
        '''
        if x_columns == None:
            x_columns = [x for x in self.numeric_list if x in self.non_missing_list and x != outcome]
        for x in x_columns:
            print('-'*100)
            print(f'{outcome} vs {x} -> rem_ol={rem_ol}')
            print('-'*100)

            # Reduce the number of columns
            data_clean = self.df[[outcome,x]]
            
            # If removal of outliers is preferred, the filter will remove all the observation lower than thres_1 percentile or higher than thres_2 percentile.
            if rem_ol:
                lim_1 = data_clean[x].quantile([thres_1]).iloc[0]
                lim_2 = data_clean[x].quantile([thres_2]).iloc[0]
                df = data_clean[(data_clean[x]>lim_1) & (data_clean[x]<lim_2)]   
            else:
                df = data_clean
            
            # Creates bins and calculates proportions of positive outcomes
            x_cat = pd.cut(df[x],bins=bins,retbins=True)
            p = df.groupby(x_cat[0], observed=False)[outcome].sum()/df.groupby(x_cat[0], observed=False)[outcome].count()
            
            # Integer indexes
            all_indexes = range(len(p))
            original_indexes = p.index
            p.index = all_indexes
            
            # Removes any bin with proportions of positive outcomes equals to 0 or 1 to avoid ln(0) or zero division. 
            p = pd.Series(p[(p.values>0) & (p.values<1)], index=p.index) 
            
            # ln(p/(1-p))
            log_odd = np.log(p/(1-p))

            # Relationships and kernel distribution graphs
            fig, axes = plt.subplots(1, 2, figsize=(10, 4))
            g = log_odd.plot(marker='o', label='Values',ax=axes[0])
            missing_indexes = log_odd.index[log_odd.isna()]
            g.scatter(missing_indexes, log_odd[log_odd.isna()])
            g.set_xticks(all_indexes)
            sns.kdeplot(data=data_clean, x=x, ax=axes[1])
            axes[0].set_title(f'ln(p/(1-p)) of {outcome} vs {bins} {x} ranges')
            axes[1].set_title(f'{x} kernel distribution')
            plt.tight_layout()
            
            # Print the intervals used to create bins
            for i, int in enumerate(original_indexes):
                print(f'{i} = {original_indexes[i]}')

            # Plot 2 Graphs
            plt.show()

    def eda_quant_uni(self, quant_var=None, type = 'hist'):
        """ 
        This function plots the univariate analysis of the quantitative variables

        Args:
            quant_var: list of quantitative variables
            type: type of plot to be used. Options are 'hist', 'box' or 'violin'
            
        """ 
        if quant_var is None:
            quant_var = self.numeric_list
        n_graphs = len(quant_var)
        n_row = math.ceil(n_graphs / 3)
        fig, axes = plt.subplots(nrows = n_row, ncols = 3, figsize=(10,n_row*3)) 
        axes=axes.flatten()
        fig.suptitle('Univariate Analysis of Quantitative Variables')
        for v, ax in zip(quant_var, axes):
            if type == 'hist':
                sns.histplot(data=self.df, x = v, ax = ax, kde=True)
            elif type == 'box':
                sns.boxplot(data=self.df, y = v, ax = ax)
            elif type == 'violin':
                sns.violinplot(data=self.df, x = v, ax = ax)
            ax.set_title(v)
        for ax in axes[n_graphs:]:
            ax.set_visible(False)
        plt.tight_layout()
        plt.show()

