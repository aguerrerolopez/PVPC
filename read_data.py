
import requests
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import pickle

indicador = str(1001)

with open('token.pkl', 'rb') as handle:
    token = pickle.load(handle)

# Hasta qué fecha fin quiero los datos
start_date = "2022-01-01"
end_date = "2022-06-02"

# URI
uri = "https://api.esios.ree.es/indicators/"+indicador+"?start_date="+start_date+"T"+ "00:00:00+02:00&end_date="+end_date+ "T"+ "23:50:00+02:00&geo_agg=sum&geo_ids&time_trunc=hour&time_agg=&locale=es"


# Read PVPC data
f = requests.get(uri, headers=token)
data = f.json()

# Store it as a dataframe
prices = pd.DataFrame(data['indicator']['values'])

################# Peninsula data
prices_pen = prices[prices['geo_name']=='Península']

# Ordinal encoder the datetime from 0 to 24.
# oe = OrdinalEncoder()
# prices_pen['datetime'] = oe.fit_transform(prices_pen['datetime'].to_numpy().reshape(-1,1))+1

#%% Plot curves
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
price_days = []

for d in np.arange(0, len(prices_pen), 24):
    price_days.append(list(prices_pen[d:d+24]['value'].values/1000))

price_days = np.vstack(price_days[:-1])

pricespd = pd.DataFrame(data=price_days, index=pd.date_range(start=start_date, end=end_date)[:-1])
pricespd.index = pricespd.index.strftime('%d/%m/%Y')
sns.heatmap(pricespd, center=0.22, cmap=sns.color_palette("coolwarm", as_cmap=True))
