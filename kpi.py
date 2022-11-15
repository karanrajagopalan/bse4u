import numpy as np
import pandas as pd
import statsmodels.api as sm
from datetime import datetime


def fit_arima_model(df, start_date, end_date, n_days, p, d=0, q=0, future=False):
    # print(df)
    if future is False:
        model = sm.tsa.ARIMA(df.iloc[0:-n_days], order=(p, d, q))
        result = model.fit()
        # print(result.predict())
        df_out = pd.DataFrame(data=[], index=df.index, columns=["predict"])
        df_out["predict"].iloc[0:-n_days] = result.predict()
        df_out["predict"].iloc[-n_days:] = result.forecast(n_days)
        return df_out, None
    else:
        model = sm.tsa.ARIMA(df, order=(p, d, q))
        result = model.fit()
        # print(result.predict())
        df_out = pd.DataFrame(data=[], index=df.index, columns=["predict"])
        df_out["predict"] = result.predict()
        fc = result.forecast(n_days)
        fc_index = get_date_index(n_days, end_date)
        df_pred = pd.DataFrame(data=fc.values, index=fc_index, columns=["predict"])
    return df_out, df_pred


def get_date_index(n_days, start_date):
    # start_date = datetime.strftime(datetime.today().date(), '%Y-%m-%d')
    end_date = datetime.strftime(start_date + pd.Timedelta(days=50), '%Y-%m-%d')
    s = pd.date_range(start_date, end_date, freq='D').to_series()
    s = s.to_frame()
    s['weekday_flag'] = [x not in [5, 6] for x in s[0].dt.weekday]
    s = s[1:]
    return s[s["weekday_flag"] is True].index[0:n_days]


class stock_kpi:
    def __init__(self, data):
        self.historic_data = data
