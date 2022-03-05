import pandas as pd
import logging
from . import utils
import yfinance as yf


def get_info(data: dict = {}, config: dict = {}, logger: object = logging.getLogger(__name__)) -> dict:
    """
    This function collectes basic stock information.

    Args:
        config (dict): Configurable Options
        data (dict): Dictionary of named Pandas Dataframes
        logger (object): Standard Python Logger

    Returns:
        Results(dict): Dictionary of output pandas dataframes
    """
    utils.validate_input_contract(data=data, config=config, logger=logger)

    # Set required Parameters
    stock_columns_list = config.setdefault('dataFields', ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap'])
    symbolField = config.setdefault('symbolField', 'symbol')

    # get input stock list
    df_input = data.setdefault('input', pd.DataFrame(columns=[symbolField])).copy()
    df_input[symbolField] = df_input[symbolField].str.upper()

    # Set Empty Data States
    raw_data = list()

    for stock_symbol in df_input[symbolField].unique():
        logger.info(f'Collecting Ticker {stock_symbol} information')
        stock_info = yf.Ticker(stock_symbol).info

        stock_data = []
        for column in stock_columns_list:
            stock_data.append(stock_info.get(column))
        raw_data.append(stock_data)

    df_stock_info = pd.DataFrame(data=raw_data, columns=stock_columns_list)

    df_stock_data = pd.merge(
        left=df_input,
        right=df_stock_info,
        how='inner',
        left_on=symbolField,
        right_on='symbol'
    )

    if len(df_stock_data.index) > 0:
        # show merge state only if there is data
        logger.info('Merged Stock Info')

    return {
        'output': df_stock_data
    }


def get_holdings(data: dict = {}, config: dict = {}, logger: object = logging.getLogger(__name__)) -> dict:
    """
    This function collectes exploded holdings stock information.

    Args:
        config (dict): Configurable Options
        data (dict): Dictionary of named Pandas Dataframes
        logger (object): Standard Python Logger

    Returns:
        Results(dict): Dictionary of output pandas dataframes
    """
    utils.validate_input_contract(data=data, config=config, logger=logger)
    symbolField = config.setdefault('symbolField', 'symbol')
    holdings = list()
    holdings_column_list = ['parent', 'symbol', 'holdingPercent']

    df_input = data.setdefault('input', pd.DataFrame(columns=[symbolField])).copy()
    df_input[symbolField] = df_input[symbolField].str.upper()

    # Check to verify stock has holdings
    # This section will need to be replaced with a pull from ZACKs as yFinance limits to the top 10 holdings.
    for stock_symbol in df_input[symbolField].unique():
        logger.info(f'Collecting Ticker {stock_symbol} holdings')
        stock_info = yf.Ticker(stock_symbol).info

        for holding in stock_info.setdefault('holdings', {}):
            holdings.append([stock_symbol, holding.get('symbol'), holding.get('holdingPercent')])

    df_holdings = pd.DataFrame(data=holdings, columns=holdings_column_list)

    # ensure that totals add to 100 Percent by adding other value
    df_other_holdings = 1 - df_holdings.groupby(['parent']).sum()
    df_other_holdings['symbol'] = None
    df_other_holdings = df_other_holdings.reset_index()

    df_holdings = pd.concat([df_holdings, df_other_holdings])

    return {
        'output': df_holdings
    }
