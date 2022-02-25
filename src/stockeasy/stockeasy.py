import pandas as pd
import logging
from . import utils
import yfinance as yf


def analyzer(data: dict = {}, config: dict = {}, logger: object = logging.getLogger('default')):
    """
    This function completes a review of a provide stock portfolio.

    Args:
        config (dict): Configurable Options
        data (dict): Dictionary of named Pandas Dataframes
        logger (object): Standard Python Logger

    Returns:
        Results(dict): Dictionary of output pandas dataframes
    """
    utils.validate_input_contract(data=data, config=config, logger=logger)

    if (config.get('method') == 'getDetails'):

        columns_list = config.get('dataFields')
        raw_data = []

        for index, row in data.get('input').iterrows():
            stock_symbol = row['symbol']
            stock_info = yf.Ticker(stock_symbol).info

            stock_data = []
            for column in columns_list:
                stock_data.append(stock_info.get(column))
            raw_data.append(stock_data)

        df_stock_data = pd.DataFrame(data=raw_data, columns=columns_list)

        return {
            'output': df_stock_data,
            'report': pd.DataFrame(['<html><body>passthrough used</body></html>'], columns=['report']),
        }

    # Assume passthrough at this point
    return {
        'output': data.get('input'),
        'report': pd.DataFrame(['<html><body>passthrough used</body></html>'], columns=['report']),
    }
