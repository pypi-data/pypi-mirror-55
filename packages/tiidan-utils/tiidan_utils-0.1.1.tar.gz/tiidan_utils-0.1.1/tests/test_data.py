import pytest
from tiidan_utils.trade_query import _Data


@pytest.fixture
def data():
    return _Data()


def test_data(data):
    print(data.china_provinces)
    print(data.china_cities)
    assert True
