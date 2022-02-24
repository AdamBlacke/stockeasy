import stockeasy
import logging


def test_init():
    assert 1 == 1


def test_analyzer_inputs():
    assert stockeasy.analyzer({}, {}, logging.getLogger('test-logger')) == 0
    assert stockeasy.analyzer('', {}, logging.getLogger('test-logger')) == 1
    assert stockeasy.analyzer({}, '', logging.getLogger('test-logger')) == 1
