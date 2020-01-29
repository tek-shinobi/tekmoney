from decimal import Decimal

import pytest

from tekmoney.currency import Currency
from tekmoney.currency_tax import CurrencyWithTax
from tekmoney.currency_range import CurrencyRange
from tekmoney.currency_range_tax import CurrencyRangeTax
from tekmoney.flat_tax import flat_tax


def test_application():
    result = flat_tax(CurrencyWithTax(Currency(10, 'BTC'), Currency(10, 'BTC')), 1)
    assert result.net == Currency(10, 'BTC')
    assert result.gross == Currency(20, 'BTC')
    result = flat_tax(Currency(100, 'BTC'), Decimal('0.5'))
    assert result.net == Currency(100, 'BTC')
    assert result.gross == Currency(150, 'BTC')
    with pytest.raises(TypeError):
        flat_tax(1, 1)


def test_tax_from_gross():
    result = flat_tax(
        CurrencyWithTax(Currency(120, 'USD'), Currency(120, 'USD')),
        Decimal('0.2'), keep_gross=True)
    assert result.net == Currency(100, 'USD')
    assert result.gross == Currency(120, 'USD')
    result = flat_tax(Currency(150, 'BTC'), Decimal('0.5'), keep_gross=True)
    assert result.net == Currency(100, 'BTC')
    assert result.gross == Currency(150, 'BTC')


def test_range():
    price_range = CurrencyRange(Currency(10, 'BTC'), Currency(20, 'BTC'))
    result = flat_tax(price_range, 1)
    assert result.start == CurrencyWithTax(Currency(10, 'BTC'), Currency(20, 'BTC'))
    assert result.stop == CurrencyWithTax(Currency(20, 'BTC'), Currency(40, 'BTC'))
    price_range = CurrencyRangeTax(
        CurrencyWithTax(Currency(10, 'BTC'), Currency(10, 'BTC')),
        CurrencyWithTax(Currency(20, 'BTC'), Currency(20, 'BTC')))
    result = flat_tax(price_range, 1)
    assert result.start == CurrencyWithTax(Currency(10, 'BTC'), Currency(20, 'BTC'))
    assert result.stop == CurrencyWithTax(Currency(20, 'BTC'), Currency(40, 'BTC'))
