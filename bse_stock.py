from constants import *
import requests
import pandas as pd
from io import StringIO

s = requests.session()

class bse_stock:
    def __init__(self,scripname,start_ts,end_ts):
        self.scripname = scripname
        self.start_ts = start_ts
        self.end_ts = end_ts
    def get_historic_data(self):
        historic_data_url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.scripname}.BO?" \
                            f"period1={self.start_ts}&period2={self.end_ts}&interval=1d&events=history&includeAdjustedClose=true"
        data_bytes = s.get(historic_data_url, headers=HEADERS)
        str_data = str(data_bytes.content, 'utf-8')
        sio = StringIO(str_data)
        return pd.read_csv(sio)
