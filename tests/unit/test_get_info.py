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
def test_get_info_data_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_info(data=df_stocklist)

    # expected data type passed
    results = stockeasy.get_info(data={'input': df_stocklist})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_info_config_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_info(config='')

    # expected data type passed
    results = stockeasy.get_info(config={'setting 1': 'Anything'})
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_info_logger_typecheck():
    # wrong data type passed
    with pytest.raises(TypeError):
        stockeasy.get_info(logger='')

    # expected data type passed
    results = stockeasy.get_info(logger=logging.getLogger('log'))
    assert isinstance(results.get('output'), pd.DataFrame)


def test_get_info_results_typecheck():
    # Verify only named dataframes are returned
    results = stockeasy.get_info(data={'input': df_stocklist})
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)


def test_get_info_verify_results():
    config = {
        'symbolField': 'symbol',
        'sharesField': 'sharesOwned',
        'dataFields': ['symbol', 'shortName']
    }

    df_expected_results = pd.DataFrame(
        [
            ['VTSAX', 120, 'Vanguard Total Stock Market Ind'],
            ['MSFT', 100, 'Microsoft Corporation']
        ],
        columns=['symbol', 'sharesOwned', 'shortName']
    )

    # Verify Run
    results = stockeasy.get_info({'input': df_stocklist}, config=config)
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)

    print(results.get('output').head())

    # Verify Results Match expectations
    assert results.get('output').equals(df_expected_results)


def test_get_info_verify_results_lower_case():
    df_stocklist_lower = pd.DataFrame([['vtsax', 120], ['msft', 100]], columns=['symbol', 'sharesOwned'])
    config = {
        'symbolField': 'symbol',
        'sharesField': 'sharesOwned',
        'dataFields': ['symbol', 'shortName']
    }

    df_expected_results = pd.DataFrame(
        [
            ['VTSAX', 120, 'Vanguard Total Stock Market Ind'],
            ['MSFT', 100, 'Microsoft Corporation']
        ],
        columns=['symbol', 'sharesOwned', 'shortName']
    )

    # Verify Run
    results = stockeasy.get_info({'input': df_stocklist_lower}, config=config)
    for item in results:
        assert isinstance(results.get(item), pd.DataFrame)

    # Verify Results Match expectations
    assert results.get('output').equals(df_expected_results)
