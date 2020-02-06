from decimal import Decimal, ROUND_DOWN
from typing import TypeVar, Union

from tekmoney.currency import Currency
from tekmoney.currency_range import CurrencyRange
from tekmoney.currency_tax import CurrencyWithTax
from tekmoney.currency_range_tax import CurrencyRangeTax

Dint = Union[Decimal, int]

T = TypeVar("T", Currency, CurrencyRange, CurrencyWithTax, CurrencyRangeTax)


def fixed_discount(base: T, discount: Currency) -> T:
    """Apply a fixed discount to any currency type."""
    if isinstance(base, CurrencyRange):
        return CurrencyRange(
            fixed_discount(base.start, discount), fixed_discount(base.stop, discount)
        )
    if isinstance(base, CurrencyRangeTax):
        return CurrencyRangeTax(
            fixed_discount(base.start, discount), fixed_discount(base.stop, discount)
        )
    if isinstance(base, CurrencyWithTax):
        return CurrencyWithTax(
            net=fixed_discount(base.net, discount),
            gross=fixed_discount(base.gross, discount),
        )
    if isinstance(base, Currency):
        return max(base - discount, Currency(0, base.currency))
    raise TypeError("Unknown base for fixed_discount: %r" % (base,))


def fractional_discount(base: T, fraction: Decimal, *, from_gross=True) -> T:
    """Apply a fractional discount based on either gross or net amount."""
    if isinstance(base, CurrencyRange):
        return CurrencyRange(
            fractional_discount(base.start, fraction, from_gross=from_gross),
            fractional_discount(base.stop, fraction, from_gross=from_gross),
        )
    if isinstance(base, CurrencyRangeTax):
        return CurrencyRangeTax(
            fractional_discount(base.start, fraction, from_gross=from_gross),
            fractional_discount(base.stop, fraction, from_gross=from_gross),
        )
    if isinstance(base, CurrencyWithTax):
        if from_gross:
            discount = (base.gross * fraction).quantize(rounding=ROUND_DOWN)
        else:
            discount = (base.net * fraction).quantize(rounding=ROUND_DOWN)
        return fixed_discount(base, discount)
    if isinstance(base, Currency):
        discount = (base * fraction).quantize(rounding=ROUND_DOWN)
        return fixed_discount(base, discount)
    raise TypeError("Unknown base for fractional_discount: %r" % (base,))


def percentage_discount(base: T, percentage: Dint, *, from_gross=True) -> T:
    """Apply a percentage discount based on either gross or net amount."""
    factor = Decimal(percentage) / 100
    return fractional_discount(base, factor, from_gross=from_gross)
