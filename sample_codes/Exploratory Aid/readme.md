# Explore Aid

This code contains functions that can help exploring a data set.

<h3 align="center"> List of functions </h3>

- **missingness** Computes the count and proportion of missing values for each column.

- **columns_df** - Creates a DataFrame summarizing column types, missing values, and unique value counts.

- **missingness_chi_whitin** - Performs a chi-square test to assess associations between missing values in different columns.

- **random_forest_importance** - Uses a Random Forest model to compute and visualize feature importance for predicting an outcome.

- **missingness_association** - Uses Random Forest to determine which variables predict missingness in other columns.

- **eda_quant_uni** - Plots univariate distributions of numeric variables using histograms, boxplots, or violin plots.

- **eda_cat_uni** - Plots univariate distributions of categorical variables using count plots.

- **eda_date_uni** - Plots univariate distributions of datetime variables.

- **eda_cat_vs_quant_bi** - Visualizes relationships between categorical and numerical variables using histograms, KDE, or violin plots.

- **eda_cat_vs_cat_bi** - Plots relationships between two categorical variables using count plots.

- **cat_bivariate** - Computes cross-tabulations and chi-square tests for relationships between categorical variables.