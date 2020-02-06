import pytest

from tekmoney.currency import Currency
from tekmoney.currency_tax import CurrencyWithTax
from tekmoney.utils import tek_sum


def test_init():
    currency = CurrencyWithTax(net=Currency(1, "USD"), gross=Currency(1, "USD"))
    assert (currency.net == Currency(1, "USD")) and (
        currency.gross == Currency(1, "USD")
    )
    with pytest.raises(ValueError):
        CurrencyWithTax(net=Currency(1, "USD"), gross=Currency(1, "GBP"))
    with pytest.raises(TypeError):
        CurrencyWithTax(1, 1)


def test_str():
    currency = CurrencyWithTax(net=Currency(1, "USD"), gross=Currency(1, "USD"))
    assert str(currency) == "CurrencyWithTax(net=1 USD, gross=1 USD)"


def test_add():
    currency1 = CurrencyWithTax(Currency(10, "USD"), Currency(15, "USD"))
    currency2 = CurrencyWithTax(Currency(20, "USD"), Currency(30, "USD"))
    assert currency2 + currency1 == CurrencyWithTax(
        Currency(30, "USD"), Currency(45, "USD")
    )
    currency3 = currency1 + Currency(5, "USD")
    assert currency3.net == Currency(15, "USD")
    assert currency3.gross == Currency(20, "USD")
    with pytest.raises(ValueError):
        currency1 + CurrencyWithTax(Currency(10, "GBP"), Currency(10, "GBP"))
    with pytest.raises(TypeError):
        currency1 + 1


def test_sub():
    currency1 = CurrencyWithTax(Currency(10, "USD"), Currency(15, "USD"))
    currency2 = CurrencyWithTax(Currency(30, "USD"), Currency(45, "USD"))
    assert currency2 - currency1 == CurrencyWithTax(
        Currency(20, "USD"), Currency(30, "USD")
    )
    currency3 = currency1 - Currency(5, "USD")
    assert currency3.net == Currency(5, "USD")
    assert currency3.gross == Currency(10, "USD")
    with pytest.raises(ValueError):
        currency1 - CurrencyWithTax(Currency(10, "GBP"), Currency(10, "GBP"))
    with pytest.raises(TypeError):
        currency1 - 1


def test_mult():
    currency1 = CurrencyWithTax(Currency(10, "EUR"), Currency(20, "EUR"))
    assert currency1 * 2 == CurrencyWithTax(Currency(20, "EUR"), Currency(40, "EUR"))
    assert 2 * currency1 == currency1 * 2
    with pytest.raises(TypeError):
        currency1 * currency1


def test_div():
    currency1 = CurrencyWithTax(Currency(10, "EUR"), Currency(20, "EUR"))
    assert currency1 / 2 == CurrencyWithTax(Currency(5, "EUR"), Currency(10, "EUR"))
    with pytest.raises(TypeError):
        currency1 / currency1


def test_comparison():
    currency = CurrencyWithTax(Currency(10, "EUR"), Currency(15, "EUR"))
    assert currency == CurrencyWithTax(Currency(10, "EUR"), Currency(15, "EUR"))
    assert currency != CurrencyWithTax(Currency(20, "EUR"), Currency(30, "EUR"))
    assert currency != CurrencyWithTax(Currency(10, "GBP"), Currency(15, "GBP"))
    assert currency != Currency(10, "EUR")
    assert currency < CurrencyWithTax(Currency(20, "EUR"), Currency(30, "EUR"))
    assert currency <= CurrencyWithTax(Currency(10, "EUR"), Currency(15, "EUR"))
    assert currency <= CurrencyWithTax(Currency(20, "EUR"), Currency(30, "EUR"))
    assert currency > CurrencyWithTax(Currency(1, "EUR"), Currency(1, "EUR"))
    assert currency >= CurrencyWithTax(Currency(10, "EUR"), Currency(15, "EUR"))
    assert currency >= CurrencyWithTax(Currency(1, "EUR"), Currency(1, "EUR"))
    assert not currency <= CurrencyWithTax(Currency(1, "EUR"), Currency(1, "EUR"))
    assert not currency >= CurrencyWithTax(Currency(20, "EUR"), Currency(30, "EUR"))
    with pytest.raises(ValueError):
        currency < CurrencyWithTax(Currency(10, "GBP"), Currency(15, "GBP"))
    with pytest.raises(TypeError):
        currency >= Currency(1, "EUR")
    with pytest.raises(TypeError):
        currency < Currency(20, "EUR")


def test_quantize():
    price = CurrencyWithTax(Currency("1.001", "EUR"), Currency("1.001", "EUR"))
    assert price.quantize() == (
        CurrencyWithTax(Currency("1.00", "EUR"), Currency("1.00", "EUR"))
    )


def test_currency():
    price = CurrencyWithTax(Currency(1, "PLN"), Currency(1, "PLN"))
    assert price.currency == "PLN"


def test_tax():
    price = CurrencyWithTax(Currency(10, "USD"), Currency(15, "USD"))
    assert price.tax == Currency(5, "USD")


def test_tek_sum():
    assert tek_sum([Currency(5, "USD"), Currency(10, "USD")]) == Currency(15, "USD")
    with pytest.raises(TypeError):
        tek_sum([])
