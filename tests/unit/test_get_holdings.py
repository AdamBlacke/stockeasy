from unittest import result
import pytest
import stockeasy
import logging
import pandas as pd


df_stocklist = pd.DataFrame([['VTSAX', 120], ['MSFT', 100]], columns=['symbol', 'sharesOwned'])
df_stocklist_meta = pd.DataFrame(columns=['symbol', 'sharesOwned'])


def test_init():
    assert 1 == 1


# Default Contract Checks
def test_get_holdings_data_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_holdings(data=df_stocklist)

    # expected data type passed
    results = stockeasy.get_holdings(data={'input': df_stocklist})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_holdings_config_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_holdings(config='')

    # expected data type passed
    results = stockeasy.get_holdings(config={'setting 1': 'Anything'})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_holdings_logger_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_holdings(logger='')

    # expected data type passed
    results = stockeasy.get_holdings(logger=logging.getLogger('log'))
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_holdings_results_typecheck():
    # Verify only named dataframes are returned
    results = stockeasy.get_holdings(data={'input': df_stocklist})
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)


def test_get_holdings_verify_results():
    config = {
        'symbolField': 'symbol',
    }
    expected_columns_list = ['parent', 'symbol', 'holdingPercent']

    # Verify Run
    results = stockeasy.get_holdings({'input': df_stocklist}, config=config)
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)

    print(results.get('output').head())
    df_results = results.get('output')

    # Verify Results Match expectations
    assert df_results.columns.values.tolist() == expected_columns_list
    assert len(df_results[df_results['parent']=='MSFT'].index) == 0
    assert len(df_results[df_results['parent']=='VSTAX'].index) >= 9
