import stockeasy
import pandas as pd

# Metadata Run
df_stocklist = pd.DataFrame(columns=['symbol', 'sharesOwned'])

config = {
    'symbolField': 'symbol',
    'sharesField': 'sharesOwned',
    'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
}

results = stockeasy.analyzer({'input': df_stocklist}, config=config)

print(results.get('output').head())

# Data Run
df_stocklist = pd.DataFrame([['VTSAX', 120], ['MSFT', 100]], columns=['symbol', 'sharesOwned'])

config = {
    'symbolField': 'symbol',
    'sharesField': 'sharesOwned',
    'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
}

results = stockeasy.analyzer({'input': df_stocklist}, config=config)

print(results.get('output').head())
