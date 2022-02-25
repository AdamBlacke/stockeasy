import stockeasy
import pandas as pd

df_stocklist = pd.DataFrame(['vtsax', 'msft'], columns=['symbol'])
config = {'method': 'getDetails', 'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']}

results = stockeasy.analyzer({'input': df_stocklist}, config=config)

results.get('output').head()
