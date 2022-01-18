from bs4 import BeautifulSoup
from constants import *
import requests
import csv
import pandas as pd
import json
from matplotlib import pyplot as plt
from datetime import datetime
from datetime import timedelta


s = requests.session()
all_indices = s.get(f"{ALL_INDEX['URL']}", headers=HEADERS, params=ALL_INDEX["PAYLOAD"])
indices_data = json.loads(all_indices.content.decode('utf-8'))
indices_data = pd.DataFrame(indices_data['RealTime'])
historic_df = pd.DataFrame(curr_data)

ind_name = "S&P BSE 200"
INDEX_SCRIPS["PAYLOAD"]["strfilter"] = ind_name
ind_scrips = s.get(INDEX_SCRIPS["URL"],params=INDEX_SCRIPS["PAYLOAD"],headers=HEADERS)
ind_scrips_data = json.loads(ind_scrips.content.decode('utf-8'))
ind_scrips_df = pd.DataFrame(ind_scrips_data["Table"])


HISTORIC["PAYLOAD"]["scripcode"] = str(scrips_all[scrips_all["Issuer Name"] == "WIPRO"].index[0])
HISTORIC["PAYLOAD"]["fromdate"] = datetime.strftime(datetime.today() - timedelta(days=365), '%Y%m%d')
HISTORIC["PAYLOAD"]["todate"] = datetime.strftime(datetime.today(), '%Y%m%d')
HISTORIC["PAYLOAD"]["flag"] = '1'

historic_data = s.get(f"{HISTORIC['URL']}", headers=HEADERS, params=HISTORIC["PAYLOAD"])

data = json.loads(historic_data.content.decode('utf-8'))
curr_data = json.loads(data['Data'])
historic_df = pd.DataFrame(curr_data)
historic_df.index = pd.to_datetime(historic_df['dttm'])
historic_df.drop(columns=['dttm'], inplace=True)

for col in historic_df.columns:
    historic_df[col] = historic_df[col].astype(float)
    plt.figure();
    plt.plot(historic_df[col])
