import feather
import dask.dataframe as dd
import pandas as pd
from multiprocessing import Pool, cpu_count

class DataOperations:

    def process_Pandas_data(self,func, df, num_processes=None):

        if num_processes == None:
            num_processes = min(df.shape[1], cpu_count())

        with Pool(num_processes) as pool:
            seq = [df[col_name] for col_name in df.columns]
            results_list = pool.map(func, seq)

            return pd.concat(results_list, axis=1)

    def read_csv_file(self,file_path):

        '''
        Read huge csv file as dask dataframe
        :param file_path: csv file parh for read process
        :return: return read dask dataframe
        '''
        data = dd.read_csv(file_path)
        df = data.compute()
        return df

    def return_unique_data(self, list_col, return_type='list'):

        '''
        return unique data from list
        :param list: a list collection
        :param return_type: return object type (list,set etc.)
        :return: a list is produced by unique elements
        '''
        set_list = sorted(set(list_col), key=list_col.index)
        if return_type == 'list':
            return list(set_list)
        else:
            return set_list

    def divide_date_to_periods(self, df, date_column, period_arr):

        for period in period_arr:
            if period.lower() == "y":
                col_name = date_column + '_year'
                df[col_name] = pd.DatetimeIndex(df[date_column]).year
            if period.lower() == "m":
                col_name = date_column + '_month'
                df[col_name] = pd.DatetimeIndex(df[date_column]).month
            if period.lower() == "d":
                col_name = date_column + '_day'
                df[col_name] = pd.DatetimeIndex(df[date_column]).day
            if period.lower() == "q":
                col_name = date_column + '_quarter'
                df[col_name] = pd.DatetimeIndex(df[date_column]).quarter

        return df

    def to_datetime(self,df,date_column,date_format='%Y-%m-%d',is_divide_periods=False):
        df[date_column] = pd.to_datetime(df[date_column], format=date_format)
        if is_divide_periods:
            df = self.divide_date_to_periods(df,date_column,['Y','M','D','Q'])
        return df






