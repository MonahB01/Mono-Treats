import os
repo = os.path.expanduser("~/Documents/GitHub/MonoSolutions/")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats

class Explorer:
    # global stat
    def __init__(self, df, Exclude_cols=None):
        self.df = df
        self.int_cols = []
        self.date_col = []
        self.float_cols = []
        self.cat_cols = []
        self.ID_cols = []
        self.exclusion_list = []
        self.col_summary = {}
        self.data_summary = {}
        self.column_grouper()
        self.summary_maker()
        if Exclude_cols is not None:
            self.exclusion_list(Exclude_cols)
    # Core functions
    def column_grouper(self):
        for i, type in enumerate(self.df.dtypes):
            if type == int:
                if len(self.df[self.df.columns[i]].unique()) >= 10:
                    self.int_cols.append(self.df.columns[i])
                else:
                    self.cat_cols.append(self.df.columns[i])
            elif type == float:
                if len(self.df[self.df.columns[i]].unique()) >= 10:
                    self.float_cols.append(self.df.columns[i])
                else:
                    self.cat_cols.append(self.df.columns[i])
  
            elif type == object:
                if self.df.columns[i].lower() in ["id", "ids", "identifier", "identifiers"]:
                    self.ID_cols.append(self.df.columns[i])
                elif len(self.df[self.df.columns[i]].unique()) >= 0.99 * len(self.df):
                    if self.df[self.df.columns[i]].apply(lambda x: isinstance(x, pd.Timestamp)).any():
                        self.date_col.append(self.df.columns[i])
                    else:
                        self.ID_cols.append(self.df.columns[i])
                else:
                    self.cat_cols.append(self.df.columns[i])
                
        return(self.int_cols, self.float_cols , self.cat_cols, self.ID_cols, self.date_col)
    
    def summary_maker(self):
        for name, item in zip(["Integer", "Float", "Categorical"],[self.int_cols, self.float_cols, self.cat_cols]):
            if len(item) == 0:
                self.col_summary[name] = "No columns of this type"
                self.data_summary[name] = "No columns of this type"

            else:
                self.col_summary[name] = item
                self.data_summary[name] = self.df[item].describe(include='all')
        
        return(self.col_summary, self.data_summary)

    def exclude_cols(self, exclude_cols):
        for col in exclude_cols:
            if col in self.df.columns:
                self.exclude_cols.append(col)
                if col in self.int_cols:
                    self.int_cols.remove(col)
                elif col in self.float_cols:
                    self.float_cols.remove(col)
                elif col in self.cat_cols:
                    self.cat_cols.remove(col)
                elif col in self.ID_cols:
                    self.ID_cols.remove(col)
                elif col in self.date_col:
                    self.date_col.remove(col)
            else:
                print(f"{col} is not a column in the dataframe and cannot be excluded.")
        
        self.summary_maker()

        return(self.exclude_cols, self.int_cols, self.float_cols, self.cat_cols, self.ID_cols, self.date_col)
        # Missing data analysis
    
    def missing_data_summary(self):
        missing_data = self.df.isnull().sum()
        missing_percentage = (missing_data / len(self.df)) * 100
        missing_summary = pd.DataFrame({'Missing Values': missing_data, 'Percentage': missing_percentage})
        print("Missing Data Summary:")
        print(missing_summary)
    
    def missing_data_col(self, col):
        if col not in self.df.columns:
            print(f"{col} is not a column in the dataframe.")
            return
        missing_count = self.df[col].isnull().sum()
        missing_percentage = (missing_count / len(self.df)) * 100
        print(f'Missing Data Summary for {col}:')
        print(f'Missing Values: {missing_count}, Percentage: {missing_percentage:.2f}%')

    def missing_data_cols(self, threshold=0.5, return_cols=False):
        missing_percentage = self.df.isnull().mean(axis=0)
        cols_to_drop = self.df.columns[missing_percentage > threshold]
        print(f'Columns with more than {threshold*100}% missing data:')
        print(cols_to_drop)
        if return_cols:
            return cols_to_drop

    def missing_data_rows(self, threshold=0.5, return_rows=False):
        missing_percentage = self.df.isnull().mean(axis=1)
        rows_to_drop = self.df[missing_percentage > threshold]
        print(f'Rows with more than {threshold*100}% missing data:')
        print(rows_to_drop)
        if return_rows:
            return rows_to_drop

    # Statistical tests
    def correlation(self, method='pearson'):
        numeric_cols = self.int_cols + self.float_cols
        if len(numeric_cols) < 2:
            print("Not enough numeric columns to compute correlation.")
            return
        corr_matrix = self.df[numeric_cols].corr(method=method)
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
        plt.title(f'Correlation Heatmap ({method.capitalize()})')
        plt.show()
    
    def normality_test(self, col, method='shapiro'):
        if col not in self.df.columns:
            print(f"{col} is not a column in the dataframe.")
            col = input(f"Please choose from the available columns: {self.df.columns.tolist()}")
            if col not in self.df.columns:
                print(f"{col} is still not a valid column. Exiting function.")
                return
        if method not in ['shapiro', 'kolmogorov', 'anderson', 'skewness', 'kurtosis', 'normal']:
            print("Unsupported method!")
            method = input("Please choose from 'shapiro', 'kolmogorov', 'anderson', 'skewness', 'kurtosis', 'normal': ")
            if method not in ['shapiro', 'kolmogorov', 'anderson', 'skewness', 'kurtosis', 'normal']:
                print("Invalid method. Exiting function.")
                return
        print(f'Kurtosis for {col}: {stats.kurtosis(self.df[col].dropna())}')
        print(f'Skewness for {col}: {stats.skew(self.df[col].dropna())}')

        if method == 'shapiro':
            stat, p = stats.shapiro(self.df[col].dropna())
            print(f'Shapiro-Wilk Test for {col}: Statistics={stat}, p-value={p}')
        
        if method == 'kolmogorov':
            stat, p = stats.kstest(self.df[col].dropna(), 'norm')
            print(f'Kolmogorov-Smirnov Test for {col}: Statistics={stat}, p-value={p}')
        
        if method == 'anderson':
            result = stats.anderson(self.df[col].dropna())
            print(f'Anderson-Darling Test for {col}: Statistic={result.statistic}')
            for i in range(len(result.critical_values)):
                sl, cv = result.significance_level[i], result.critical_values[i]
                if result.statistic < cv:
                    print(f'Significance Level: {sl}, Critical Value: {cv} => Data looks normal (fail to reject H0)')
                else:
                    print(f'Significance Level: {sl}, Critical Value: {cv} => Data does not look normal (reject H0)')
            
        if method == 'skewness':
            result = stats.skewtest(self.df[col].dropna())
            print(f'Skewness Test for {col}: Statistic={result.statistic}, p-value={result.pvalue}')
        
        if method == 'kurtosis':
            result = stats.kurtosistest(self.df[col].dropna())
            print(f'Kurtosis Test for {col}: Statistic={result.statistic}, p-value={result.pvalue}')

        if method == 'normal':
            result = stats.normaltest(self.df[col].dropna())
            print(f'Normality Test for {col}: Statistic={result.statistic}, p-value={result.pvalue}')

    def outlier_detection(self, col, method='zscore', threshold=3, return_values=False):
        if col not in self.df.columns:
            print(f"{col} is not a column in the dataframe.")
            return
        if method == 'zscore':
            z_scores = np.abs(stats.zscore(self.df[col].dropna()))
            outliers = self.df[col][z_scores > threshold]
            print(f'Outliers detected in {col} using Z-score method (threshold={threshold}):')
            print(outliers)
        elif method == 'iqr':
            q1 = self.df[col].quantile(0.25)
            q3 = self.df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            outliers = self.df[(self.df[col] < lower_bound) | (self.df[col] > upper_bound)][col]
            print(f'Outliers detected in {col} using IQR method (threshold={threshold}):')
            print(outliers)
            if return_values:
                return outliers
        else:
            print("Unsupported method. Please use 'zscore' or 'iqr'.")

    def ttest(self, col1, col2):
        if col1 not in self.df.columns or col2 not in self.df.columns:
            print(f"One or both columns {col1}, {col2} are not in the dataframe.")
            return
        statistic, p = stats.ttest_ind(self.df[col1].dropna(), self.df[col2].dropna())
        print(f'T-test between {col1} and {col2}: \n Statistics={statistic}, p-value={p}')
    
    def anova(self, *cols, ad_hoc=False):
        for col in cols:
            if col not in self.df.columns:
                print(f"{col} is not a column in the dataframe.")
                return
        data = [self.df[col].dropna() for col in cols]
        statistic, p = stats.f_oneway(*data)
        print(f'ANOVA test for columns {cols}: \n Statistics={statistic}, p-value={p}')
        if ad_hoc:
            print("Performing ad-hoc tests...")
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    col1, col2 = cols[i], cols[j]
                    self.ttest(col1, col2)

    # Data Cleaning functions
    def remove_outliers(self, col, method='zscore', threshold=3):
        outliers = self.outlier_detection(col, method=method, threshold=threshold, return_values=True)
        if outliers is not None:
            self.df = self.df[~self.df[col].isin(outliers)]
            print(f"Removed {len(outliers)} outliers from {col}.")
        else:
            print(f"No outliers detected in {col} using {method} method at threshold {threshold}.")

    # Plotting functions
    def summary_plots(self):
        for name, summary in self.data_summary.items():
            if type(summary) == str:
                print(f"No columns of type {name} to stratify.")
                continue

            print(f"Summary for {name} columns:")
            print(summary)
            print("\n")
            if name == "Categorical":
                for col in self.col_summary[name]:
                    if len(self.df[col].unique()) > 30:
                        print(f"Column {col} has more than 30 unique values, skipping plot.")
                        continue
                    plt.figure(figsize=(10, 6))
                    sns.countplot(x=self.df[col])
                    plt.title(col)
                    plt.xticks(rotation=30, ha='right')
                    plt.show()
            else:
                try:
                    plot_df = self.df[self.col_summary[name]]
                    sns.pairplot(plot_df, kind='scatter')
                    plt.show()
                except:
                    print(f"Not enough columns to plot for {name} type.")
                    sns.histplot(data=self.df[self.col_summary[name]], x=self.col_summary[name][0], kde=True)
                    plt.show()

    def stratified_plots(self, stratify_col):
        working_df = self.df.copy()
        if stratify_col not in self.df.columns:
            print(f"{stratify_col} is not a column in the dataframe.")
            return
        for name, columns in self.col_summary.items():
            if type(columns) == str:
                print(f"No columns of type {name} to stratify.")
                continue
            if name == "Categorical":
                for col in self.col_summary[name]:
                    if col == stratify_col:
                        continue
                    elif len(self.df[col].unique()) > 30:
                        print(f"Column {col} has more than 30 unique values, skipping plot/summary.")
                        working_df.drop(columns=col, inplace=True)
                        continue
                    plt.figure(figsize=(10, 6))
                    sns.countplot(x=self.df[col], hue=self.df[stratify_col])
                    plt.title(col)
                    plt.xticks(rotation=30, ha='right')
                    plt.legend(title=stratify_col)
                    plt.show()
                
                grouped = working_df.groupby(stratify_col)
                print(f"Stratified Summary for {name} columns by {stratify_col}:")
                print(grouped.describe(include='all'))
                print("\n")

            else:
                print(f"Stratified Summary for {name} columns by {stratify_col}:")
                print(working_df[columns].describe(include='all'))
                print("\n")

                try:
                    plot_df = self.df[self.col_summary[name] + [stratify_col]]
                    sns.pairplot(plot_df, hue=stratify_col, kind='scatter')
                    plt.show()
                except:
                    print(f"Not enough columns to pairplot for {name} type.")
                    sns.histplot(data=self.df[self.col_summary[name]], x=self.col_summary[name][0], hue=self.df[stratify_col], kde=True)
                    plt.show()
