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
logger.info(f'executed get_info metadata run in {(end_time-start_time):.4f}s')

start_time = time()
results = stockeasy.get_holdings({'input': df_stocklist}, config={'symbolField': 'symbol'})
end_time = time()
logger.info(f'executed get_holdings metadata run in {(end_time-start_time):.4f}s')

# Data Run
# Get Stock Information Smoke Test
df_stocklist = pd.DataFrame([['vtsax', 120], ['msft', 100], ['swtsx', 100], ['xlu', 100]], columns=['symbol', 'sharesOwned'])
# df_stocklist = pd.DataFrame([['xlu', 100]], columns=['symbol', 'sharesOwned'])
# df_stocklist = pd.DataFrame([['vtsax', 100]], columns=['symbol', 'sharesOwned'])

config = {
    'symbolField': 'symbol',
    'sharesField': 'sharesOwned',
    'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
}
results = stockeasy.get_info({'input': df_stocklist}, config=config)

# Get Stock Holdings Smoke Test
config = {
    'symbolField': 'symbol'
}

results = stockeasy.get_holdings({'input': df_stocklist}, config=config)
# print(results.get('output'))

logger.info('Completed Smoke Test.')
