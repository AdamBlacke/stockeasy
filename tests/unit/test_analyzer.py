from unittest import result
import pytest
import stockeasy
import logging
import pandas as pd


df_stocklist = pd.DataFrame([['vtsax', 120], ['msft', 100]], columns=['symbol', 'sharesOwned'])
df_stocklist_meta = pd.DataFrame(columns=['symbol', 'sharesOwned'])


def test_init():
    assert 1 == 1


# Default Contract Checks
def test_analyzer_data_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.analyzer(data=df_stocklist)

    # expected data type passed
    results = stockeasy.analyzer(data={'input': df_stocklist})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_analyzer_config_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.analyzer(config='')

    # expected data type passed
    results = stockeasy.analyzer(config={'setting 1': 'Anything'})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_analyzer_logger_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.analyzer(logger='')

    # expected data type passed
    results = stockeasy.analyzer(logger=logging.getLogger('log'))
    assert isinstance(results.get('output'), pd.DataFrame)


def test_analyzer_results_typecheck():
    # Verify only named dataframes are returned
    results = stockeasy.analyzer(data={'input': df_stocklist})
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)


def test_analyzer_data_collection():
    config = {
        'symbolField': 'symbol',
        'sharesField': 'sharesOwned',
        'dataFields': ['exchange', 'symbol', 'shortName', 'sector', 'country', 'marketCap']
    }
    results = stockeasy.analyzer({'input': df_stocklist}, config=config)
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)
