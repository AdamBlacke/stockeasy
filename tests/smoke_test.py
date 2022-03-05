import stockeasy
import pandas as pd
from time import time
import logging

# set logging
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info('Starting Smoke Test')

# Metadata Run
df_stocklist = pd.DataFrame(columns=['symbol', 'sharesOwned'])

config = {
    'symbolField': 'symbol',
    'sharesField': 'sharesOwned',
    'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
}

start_time = time()
results = stockeasy.get_info({'input': df_stocklist}, config=config)
end_time = time()
print(f'executed in {(end_time-start_time):.4f}s')
print(results.get('output').head())

# Data Run
# df_stocklist = pd.DataFrame([['VTSAX', 120], ['MSFT', 100]], columns=['symbol', 'sharesOwned'])
df_stocklist = pd.DataFrame([['vtsax', 120], ['msft', 100]], columns=['symbol', 'sharesOwned'])

config = {
    'symbolField': 'symbol',
    'sharesField': 'sharesOwned',
    'exploded': True,
    'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
}

results = stockeasy.get_info({'input': df_stocklist}, config=config)

print(results.get('output'))
# print(results.get('holdings'))
