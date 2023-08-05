import numpy as np
import pandas as pd
import swifter

class DataCleaner():

    def _getDuplicateColumns(self, df,verbose=False):
        groups = df.columns.to_series().groupby(df.dtypes).groups
        duplicated_columns = []
        for dtype, col_names in groups.items():
           column_values = df[col_names]
           num_columns = len(col_names)
           for i in range(num_columns):
               column_i = column_values.iloc[:,i].values
               for j in range(i + 1, num_columns):
                   column_j = column_values.iloc[:,j].values
                   if np.array_equal(column_i, column_j):
                       if verbose:
                           print("column {} is a duplicate of column {}".format(col_names[i], col_names[j]))
                       duplicated_columns.append(col_names[i])
                       break

        return duplicated_columns

    def remove_columns(self, df, columns=None):
        '''
        Removes selected columns from selected dataframe
        :param df: Dataframe which was removed selected columns
        :param columns: The columns that were removed from selected Dataframe
        :return: dataframe: Dataframe that we removed unnecessary columns
        '''
        if columns != None:
            if type(df) == type(pd.DataFrame()):
                df.drop(columns, axis=1, inplace=True)

                return df
            else:
                raise TypeError('df parameter must be Pandas Dataframe')
        else:
            return "Columns name are empty!!"

    def remove_rows_by_condition(self,df, dict):
        '''
        Filter selected DataFrame by given dictionary key('columnName') and value('condition')
        :param df: Pandas Dataframe which will be filtered
        :param dict: Dictionary which has column name and condition
        :return: New filtered dataframe
        '''
        if dict != None:
            if type(df) == type(pd.DataFrame()):
                new_df = df.copy()
                for column, condition in dict.items():
                    f = lambda x: eval(condition)
                    new_df = new_df.loc[new_df[column].swifter.apply(f)]

                return  new_df

    def remove_outliers(self, df, low,high):
        low = low
        high = high
        quant_df = df.quantile([low, high])
        for name in list(df.columns):
            if pd.api.types.is_numeric_dtype(df[name]):
                df = df[(df[name] > quant_df.loc[low, name])
                        & (df[name] < quant_df.loc[high, name])]
        return df

    #TODO remove unique columns
    def remove_unique_columns(self,df):
        for i in df.columns:
            if len(df[i].unique()) == 1:
                df = df.drop(i, axis=1)

        return df

    #TODO remove duplicate columns
    def remove_duplicates(self, df):
        df = df.drop_duplicates()
        df = df.drop(columns=self._getDuplicateColumns(df))

        return df


