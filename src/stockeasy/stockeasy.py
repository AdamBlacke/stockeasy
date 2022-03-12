from distutils.command.build import build
import pandas as pd
import logging
from . import utils
import yfinance as yf
import requests
import re


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
    holdings_column_list = ['parent', 'symbol', 'as_of', 'sharesHeld', 'marketValue', 'holdingPercent', 'name', 'issue']
    url_list = config.setdefault('url', ["https://www.zacks.com/funds/mutual-fund/quote/{}/holding", "https://www.zacks.com/funds/etf/{}/holding"])

    url_extract_regex = {
        "https://www.zacks.com/funds/mutual-fund/quote/{}/holding": {
            'parser_table': r'(?:document.table_data.*?=.*?\[)(.*?)(?:\n)',
            'parser_row': r'(?:\[)(.*?)(?:\])',
            'parser_field': r'(?:\")(.*?)(?:\")',
            'field_cleaner': r'(?:<span class=%22hoverquote-symbol%22>)(.*?)(?:<span)'
        },
        "https://www.zacks.com/funds/etf/{}/holding": {
            'parse_table': r'(?:etf_holdings.formatted_data.*?=.*?\[)(.*?)(?:\n)',
            'parser_row': r'(?:\[)(.*?)(?:\])',
            'parser_field': r'',
            'field_cleaner': r'(.*)'
        }
    }

    df_input = data.setdefault('input', pd.DataFrame(columns=[symbolField])).copy()
    df_input[symbolField] = df_input[symbolField].str.upper()

    # Check to verify stock has holdings
    # This section will need to be replaced with a pull from ZACKs as yFinance limits to the top 10 holdings.
    for stock_symbol in df_input[symbolField].unique():
        logger.info(f'Collecting Ticker {stock_symbol} holdings')

        # Connect Session
        with requests.Session() as req:
            req.headers.update({"User-Agent": "Mozilla/5.0 (compatible; Bot/0.1; )"})
            for url in url_list:
                # url specific parser / builder
                parser_table = url_extract_regex[url].get('parser_table')
                parser_row = url_extract_regex[url].get('parser_row')
                parser_field = url_extract_regex[url].get('parser_field')
                field_cleaner = url_extract_regex[url].get('field_cleaner')

                # Get data from website
                request_result = req.get(url.format(stock_symbol))

                # Extract Tables
                logging.debug(f'parser settings:\n     Table: {parser_table}\n     Row: {parser_row}\n     Field: {parser_field}\n     Cleaner: {field_cleaner}\n')

                # If parser exists
                if parser_table:
                    tables = re.findall(parser_table, request_result.text)

                    # If tables are found
                    if len(tables) > 0:
                        for table in tables:
                            rows = re.findall(parser_row, table)
                            for row in rows:
                                # Set parent symbol key
                                row_data = [stock_symbol]
                                row = str.replace(row, '\\"', "%22")
                                fields = re.findall(parser_field, row)
                                for field in fields:
                                    field_search = re.findall(field_cleaner, field)
                                    if len(field_search) > 0:
                                        row_data.append(field_search[0])
                                    else:
                                        row_data.append(field)

                        # Parse raw data into List
                        holdings.append(row_data)

    logging.info(holdings)
    df_holdings = pd.DataFrame(data=holdings, columns=holdings_column_list)
    df_holdings['marketValue'] = pd.to_numeric(df_holdings['marketValue'].replace(',', '', regex=True))
    df_holdings['holdingPercent'] = pd.to_numeric(df_holdings['holdingPercent'].replace('%', '', regex=True)) / 100

    print(df_holdings)

    return {
        'output': df_holdings
    }
