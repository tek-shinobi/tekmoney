import pytest

from tekmoney.currency import Currency


def test_str():
    currency = Currency(5, 'USD')
    assert str(currency) == '5 USD'
