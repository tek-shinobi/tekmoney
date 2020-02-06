from functools import partial
from decimal import Decimal
import pytest

from tekmoney.currency import Currency
from tekmoney.currency_range import CurrencyRange
from tekmoney.currency_tax import CurrencyWithTax
from tekmoney.currency_range_tax import CurrencyRangeTax
from tekmoney.discount import fixed_discount, fractional_discount, percentage_discount


def test_application():
    price = CurrencyWithTax(Currency(30, "BTC"), Currency(30, "BTC"))
    discount = partial(fixed_discount, discount=Currency(10, "BTC"))
    result = discount(price)
    assert result.net == Currency(20, "BTC")
    assert result.gross == Currency(20, "BTC")
    price_range = CurrencyRange(price.net, price.net)
    result = discount(price_range)
    assert result.start == Currency(20, "BTC")
    assert result.stop == Currency(20, "BTC")
    price_range = CurrencyRangeTax(price, price)
    result = discount(price_range)
    assert result.start == CurrencyWithTax(Currency(20, "BTC"), Currency(20, "BTC"))
    assert result.stop == CurrencyWithTax(Currency(20, "BTC"), Currency(20, "BTC"))
    with pytest.raises(TypeError):
        discount(1)


def test_zero_clipping():
    price = CurrencyWithTax(Currency(10, "USD"), Currency(10, "USD"))
    result = fixed_discount(price, Currency(30, "USD"))
    assert result.net == Currency(0, "USD")
    assert result.gross == Currency(0, "USD")


def test_discount():
    price = CurrencyWithTax(Currency(100, "BTC"), Currency(100, "BTC"))
    discount = partial(fractional_discount, fraction=Decimal("0.25"))
    result = discount(price)
    assert result.net == Currency(75, "BTC")
    assert result.gross == Currency(75, "BTC")
    price_range = CurrencyRangeTax(price, price)
    result = discount(price_range)
    assert result.start == CurrencyWithTax(Currency(75, "BTC"), Currency(75, "BTC"))
    assert result.stop == CurrencyWithTax(Currency(75, "BTC"), Currency(75, "BTC"))
    result = discount(Currency(100, "BTC"))
    assert result == Currency(75, "BTC")
    with pytest.raises(TypeError):
        discount(100)


def test_discount_from_net():
    price = CurrencyWithTax(Currency(100, "PLN"), Currency(200, "PLN"))
    result = fractional_discount(price, Decimal("0.5"), from_gross=False)
    assert result.net == Currency(50, "PLN")
    assert result.gross == Currency(150, "PLN")


def test_currency_mismatch():
    with pytest.raises(ValueError):
        fixed_discount(
            CurrencyWithTax(Currency(10, "BTC"), Currency(10, "BTC")),
            Currency(10, "USD"),
        )


def test_percentage_discount():
    price = CurrencyWithTax(Currency(100, "BTC"), Currency(100, "BTC"))
    discount = partial(percentage_discount, percentage=10)
    result = discount(price)
    assert result.net == Currency(90, "BTC")
    assert result.gross == Currency(90, "BTC")
    price_range = CurrencyRangeTax(price, price)
    result = discount(price_range)
    assert result.start == CurrencyWithTax(Currency(90, "BTC"), Currency(90, "BTC"))
    assert result.stop == CurrencyWithTax(Currency(90, "BTC"), Currency(90, "BTC"))


def test_precision():
    price = CurrencyWithTax(Currency("1.01", "BTC"), Currency("1.01", "BTC"))
    result = percentage_discount(price, percentage=50)
    assert result.net == Currency("0.51", "BTC")
    assert result.net == Currency("0.51", "BTC")
