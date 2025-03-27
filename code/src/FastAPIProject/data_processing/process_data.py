import pandas as pd
from currency_converter.currency_convert import CurrencyConverter

class DataProcessing:
    _file_location = ''
    _data_frame = None
    def __init__(self,file_location):
        self._file_location = file_location
    def __read_data(self):
        if self._data_frame is None:
            file_path = self._file_location
            df = pd.read_csv(file_path)
            self._data_frame = df
            return df
        else:
            return self._data_frame
    def process_data_cleanup(self, columns=None,test_columns=None):
        if columns is None:
            columns = ['As of Date', 'Primary Account', 'Secondary Account','Comments']
        df = self.__read_data()
        df =df.drop(columns, axis=1)
        df["Match Status"] = df["Match Status"].apply(lambda x: 1 if x.lower == "break" else 0).astype(int)
        unique_currencies = df['Currency'].unique()
        convert_currency = CurrencyConverter()
        conversion_rates = convert_currency.get_conversion_rates(unique_currencies)
        x_test,y_test=None,None
        if test_columns is not None:
            try:
                y_test = df[test_columns]
                y_test = y_test.apply(lambda x: 1 if x.lower() == "yes" else 0).astype(int)
                x_test = df.drop(test_columns, axis=1)
            except Exception as e:
                print("Key Error",e)
        else:
            x_test = df

        x_test['GL Balance'] = x_test.apply(lambda row: round(row['GL Balance'] / conversion_rates.get(row['Currency'], 1), 2), axis=1)
        x_test['Ihub Balance'] = x_test.apply(lambda row: round(row['Ihub Balance'] / conversion_rates.get(row['Currency'], 1), 2), axis=1)
        x_test['Balance Difference'] = x_test.apply(lambda row: round(row['Balance Difference'] / conversion_rates.get(row['Currency'], 1), 2), axis=1)

        x_test=x_test.drop(columns=["Currency"], axis=1)

        return x_test,y_test


    def get_data_frame(self):
        return self.__read_data()







