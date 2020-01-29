import pytest
from decimal import Decimal
from tekmoney.currency import Currency


def test_str():
    currency = Currency(5, 'USD')
    assert str(currency) == '5 USD'


def test_bool():
    assert not Currency(0, 'USD')
    assert Currency(1, 'GBP')


def test_div():
    assert Currency(12, 'USD') / Currency(6, 'USD') == Decimal(2)
    assert Currency(12, 'USD') / Decimal('2') == Currency(6, 'USD')


def test_add():
    assert Currency(5, 'USD') + Currency(6, 'USD') == Currency(11, 'USD')
    assert not Currency(5, 'USD') + Currency(6, 'USD') == Currency(12, 'USD')
    with pytest.raises(ValueError):
        Currency(5, 'USD') + Currency(6, 'GBP')


def test_sub():
    assert Currency(6, 'USD') - Currency(6, 'USD') == Currency(0, 'USD')
    assert Currency(5, 'USD') - Currency(4, 'USD') == Currency(1, 'USD')
    assert not Currency(5, 'USD') - Currency(4, 'USD') == Currency(3, 'USD')
    with pytest.raises(ValueError):
        Currency(5, 'USD') - Currency(6, 'GBP')


def test_mul():
    assert Currency(6, 'USD') * 5 == Currency(30, 'USD')
    assert 5 * Currency(4, 'USD') == Currency(20, 'USD')
    assert not Currency(5, 'USD') * 8 == Currency(3, 'USD')


def test_lt():
    assert Currency(5, 'USD') < Currency(6, 'USD')
    assert not Currency(7, 'USD') < Currency(6, 'USD')
    with pytest.raises(ValueError):
        Currency(6, 'USD') < Currency(6, 'GBP')


def test_le():
    assert Currency(5, 'USD') <= Currency(5, 'USD')
    assert Currency(5, 'USD') <= Currency(6, 'USD')
    assert not Currency(7, 'USD') <= Currency(6, 'USD')
    with pytest.raises(ValueError):
        Currency(6, 'USD') <= Currency(6, 'GBP')


def test_gt():
    assert not Currency(5, 'USD') > Currency(6, 'USD')
    assert Currency(7, 'USD') > Currency(6, 'USD')
    with pytest.raises(ValueError):
        Currency(6, 'USD') > Currency(6, 'GBP')


def test_ge():
    assert Currency(5, 'USD') >= Currency(5, 'USD')
    assert not Currency(5, 'USD') >= Currency(6, 'USD')
    assert Currency(7, 'USD') >= Currency(6, 'USD')
    with pytest.raises(ValueError):
        Currency(6, 'USD') >= Currency(6, 'GBP')


def test_quantize():
    assert str(Currency(1, 'USD').quantize().amount) == '1.00'
    assert str(Currency(1, 'USD').quantize('.001').amount) == '1.000'
    assert str(Currency(Decimal(1.001), 'USD').quantize('.001').amount) == '1.001'
    assert str(Currency(Decimal(1.001), 'USD').quantize('.01').amount) == '1.00'

