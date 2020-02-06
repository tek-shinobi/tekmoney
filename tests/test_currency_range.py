import pytest

from tekmoney.currency import Currency
from tekmoney.currency_range import CurrencyRange


def test_construction():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    assert price_range.start == price1
    assert price_range.stop == price2
    with pytest.raises(ValueError):
        CurrencyRange(price1, Currency(20, "PLN"))
    with pytest.raises(ValueError):
        CurrencyRange(price2, price1)


def test_addition_with_money():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    price3 = Currency(40, "EUR")
    result = price_range + price3
    assert result.start == price1 + price3
    assert result.stop == price2 + price3
    with pytest.raises(ValueError):
        price_range + Currency(1, "BTC")


def test_addition_with_money_range():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range1 = CurrencyRange(price1, price2)
    price3 = Currency(40, "EUR")
    price4 = Currency(80, "EUR")
    price_range2 = CurrencyRange(price3, price4)
    result = price_range1 + price_range2
    assert result.start == price1 + price3
    assert result.stop == price2 + price4
    with pytest.raises(ValueError):
        price_range1 + CurrencyRange(Currency(1, "BTC"), Currency(2, "BTC"))


def test_addition_with_other_types():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    with pytest.raises(TypeError):
        price_range + 1


def test_subtraction_with_money():
    price1 = Currency(40, "EUR")
    price2 = Currency(80, "EUR")
    price_range = CurrencyRange(price1, price2)
    price3 = Currency(10, "EUR")
    result = price_range - price3
    assert result.start == price1 - price3
    assert result.stop == price2 - price3
    with pytest.raises(ValueError):
        price_range - Currency(1, "BTC")


def test_subtraction_with_money_range():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range1 = CurrencyRange(price1, price2)
    price3 = Currency(40, "EUR")
    price4 = Currency(80, "EUR")
    price_range2 = CurrencyRange(price3, price4)
    result = price_range2 - price_range1
    assert result.start == price3 - price1
    assert result.stop == price4 - price2
    with pytest.raises(ValueError):
        price_range2 - CurrencyRange(Currency(1, "BTC"), Currency(2, "BTC"))


def test_subtraction_with_other_types():
    price1 = Currency(40, "EUR")
    price2 = Currency(80, "EUR")
    price_range = CurrencyRange(price1, price2)
    with pytest.raises(TypeError):
        price_range - 1


def test_comparison():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range1 = CurrencyRange(price1, price2)
    price3 = Currency(40, "EUR")
    price4 = Currency(80, "EUR")
    price_range2 = CurrencyRange(price3, price4)
    assert price_range1 == CurrencyRange(price1, price2)
    assert price_range1 != price_range2
    assert price_range1 != CurrencyRange(price1, price1)
    assert price_range1 != CurrencyRange(Currency(10, "USD"), Currency(30, "USD"))
    assert price_range1 != price1


def test_membership():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    assert price1 in price_range
    assert price2 in price_range
    assert (price1 + price2) / 2 in price_range
    assert price1 + price2 not in price_range
    with pytest.raises(TypeError):
        15 in price_range


def test_quantize():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    result = price_range.quantize()
    assert str(result.start.amount) == "10.00"
    assert str(result.stop.amount) == "30.00"


def test_replace():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price3 = Currency(20, "EUR")
    price_range = CurrencyRange(price1, price2)
    result = price_range.replace(stop=price3)
    assert result.start == price1
    assert result.stop == price3
    result = price_range.replace(start=price3)
    assert result.start == price3
    assert result.stop == price2


def test_currency():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    assert price_range.currency == "EUR"


def test_str():
    price1 = Currency(10, "EUR")
    price2 = Currency(30, "EUR")
    price_range = CurrencyRange(price1, price2)
    assert str(price_range) == ("CurrencyRange(10 EUR 30 EUR)")
