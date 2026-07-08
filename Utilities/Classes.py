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

    def stratify_plots(self, stratify_col):
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
            return
        if method == 'shapiro':
            statistic, p = stats.shapiro(self.df[col].dropna())
            print(f'Shapiro-Wilk Test for {col}: \n Statistics={statistic}, p-value={p}')
        elif method == 'ks':
            statistic, p = stats.kstest(self.df[col].dropna(), 'norm')
            print(f'Kolmogorov-Smirnov Test for {col}: \n Statistics={statistic}, p-value={p}')
        else:
            print("Unsupported method. Please use 'shapiro' or 'kolmogorov-smirnov'.")

