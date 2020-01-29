import pytest

from tekmoney.currency import Currency
from tekmoney.currency_range import CurrencyRange
from tekmoney.currency_tax import CurrencyWithTax
from tekmoney.currency_range_tax import CurrencyRangeTax


def test_construction():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    assert price_range.start == price1
    assert price_range.stop == price2
    with pytest.raises(ValueError):
        CurrencyRangeTax(price1, CurrencyWithTax(Currency(20, 'PLN'), Currency(20, 'PLN')))
    with pytest.raises(ValueError):
        CurrencyRangeTax(price2, price1)


def test_addition_with_money():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    price3 = Currency(40, 'EUR')
    result = price_range + price3
    assert result.start == price1 + price3
    assert result.stop == price2 + price3
    with pytest.raises(ValueError):
        price_range + Currency(1, 'BTC')


def test_addition_with_money_range():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range1 = CurrencyRangeTax(price1, price2)
    price3 = Currency(40, 'EUR')
    price4 = Currency(80, 'EUR')
    price_range2 = CurrencyRange(price3, price4)
    result = price_range1 + price_range2
    assert result.start == price1 + price3
    assert result.stop == price2 + price4
    with pytest.raises(ValueError):
        price_range1 + CurrencyRange(Currency(1, 'BTC'), Currency(2, 'BTC'))


def test_addition_with_taxed_money():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    price3 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    result = price_range + price3
    assert result.start == price1 + price3
    assert result.stop == price2 + price3
    with pytest.raises(ValueError):
        price_range + CurrencyWithTax(Currency(1, 'BTC'), Currency(1, 'BTC'))


def test_addition_with_taxed_money_range():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range1 = CurrencyRangeTax(price1, price2)
    price3 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price4 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range2 = CurrencyRangeTax(price3, price4)
    result = price_range1 + price_range2
    assert result.start == price1 + price3
    assert result.stop == price2 + price4
    with pytest.raises(ValueError):
        price_range1 + CurrencyRangeTax(
            CurrencyWithTax(Currency(1, 'BTC'), Currency(1, 'BTC')),
            CurrencyWithTax(Currency(2, 'BTC'), Currency(2, 'BTC')))


def test_addition_with_other_types():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    with pytest.raises(TypeError):
        price_range + 1


def test_subtraction_with_money():
    price1 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price2 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    price3 = Currency(10, 'EUR')
    result = price_range - price3
    assert result.start == price1 - price3
    assert result.stop == price2 - price3
    with pytest.raises(ValueError):
        price_range - Currency(1, 'BTC')


def test_subtraction_with_money_range():
    price1 = Currency(10, 'EUR')
    price2 = Currency(30, 'EUR')
    price_range1 = CurrencyRange(price1, price2)
    price3 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price4 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range2 = CurrencyRangeTax(price3, price4)
    result = price_range2 - price_range1
    assert result.start == price3 - price1
    assert result.stop == price4 - price2
    with pytest.raises(ValueError):
        price_range2 - CurrencyRange(Currency(1, 'BTC'), Currency(2, 'BTC'))


def test_subtraction_with_taxed_money():
    price1 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price2 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    price3 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    result = price_range - price3
    assert result.start == price1 - price3
    assert result.stop == price2 - price3
    with pytest.raises(ValueError):
        price_range - CurrencyWithTax(Currency(1, 'BTC'), Currency(1, 'BTC'))


def test_subtraction_with_taxed_money_range():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range1 = CurrencyRangeTax(price1, price2)
    price3 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price4 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range2 = CurrencyRangeTax(price3, price4)
    result = price_range2 - price_range1
    assert result.start == price3 - price1
    assert result.stop == price4 - price2
    with pytest.raises(ValueError):
        price_range2 - CurrencyRangeTax(
            CurrencyWithTax(Currency(1, 'BTC'), Currency(1, 'BTC')),
            CurrencyWithTax(Currency(2, 'BTC'), Currency(2, 'BTC')))


def test_subtraction_with_other_types():
    price1 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price2 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    with pytest.raises(TypeError):
        price_range - 1


def test_comparison():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range1 = CurrencyRangeTax(price1, price2)
    price3 = CurrencyWithTax(Currency(40, 'EUR'), Currency(60, 'EUR'))
    price4 = CurrencyWithTax(Currency(80, 'EUR'), Currency(120, 'EUR'))
    price_range2 = CurrencyRangeTax(price3, price4)
    assert price_range1 == CurrencyRangeTax(price1, price2)
    assert price_range1 != price_range2
    assert price_range1 != CurrencyRangeTax(price1, price1)
    assert price_range1 != CurrencyRangeTax(
        CurrencyWithTax(Currency(10, 'USD'), Currency(15, 'USD')),
        CurrencyWithTax(Currency(30, 'USD'), Currency(45, 'USD')))
    assert price_range1 != price1


def test_membership():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    assert price1 in price_range
    assert price2 in price_range
    assert (price1 + price2) / 2 in price_range
    assert price1 + price2 not in price_range
    with pytest.raises(TypeError):
        15 in price_range


def test_quantize():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    result = price_range.quantize()
    assert str(result.start.net.amount) == '10.00'
    assert str(result.stop.net.amount) == '30.00'


def test_replace():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price3 = CurrencyWithTax(Currency(20, 'EUR'), Currency(30, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    result = price_range.replace(stop=price3)
    assert result.start == price1
    assert result.stop == price3
    result = price_range.replace(start=price3)
    assert result.start == price3
    assert result.stop == price2


def test_currency():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    assert price_range.currency == 'EUR'


def test_repr():
    price1 = CurrencyWithTax(Currency(10, 'EUR'), Currency(15, 'EUR'))
    price2 = CurrencyWithTax(Currency(30, 'EUR'), Currency(45, 'EUR'))
    price_range = CurrencyRangeTax(price1, price2)
    assert str(price_range) == (
        "CurrencyRangeTax(CurrencyWithTax(net=10 EUR, gross=15 EUR), CurrencyWithTax(net=30 EUR, gross=45 EUR))"
    )
