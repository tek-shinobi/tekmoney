from decimal import Decimal
from typing import Optional, Union, overload

from .currency import Currency
from .currency_range import CurrencyRange
from .currency_tax import CurrencyWithTax
from .currency_range_tax import CurrencyRangeTax

Dint = Union[Decimal, int]


@overload
def flat_tax(
        base: Union[Currency, CurrencyWithTax],
        tax_rate: Decimal,
        *,
        keep_gross) -> CurrencyWithTax:
    ...  # pragma: no cover


@overload
def flat_tax(
        base: Union[CurrencyRange, CurrencyRangeTax],
        tax_rate: Decimal,
        *,
        keep_gross) -> CurrencyRangeTax:
    ...  # pragma: no cover


def flat_tax(base, tax_rate, *, keep_gross=False):
    """Apply a flat tax by either increasing gross or decreasing net amount.
    If keep_gross True, gross constant, net amount decreased"""
    fraction = Decimal(1) + tax_rate
    if isinstance(base, (CurrencyRange, CurrencyRangeTax)):
        return CurrencyRangeTax(
            flat_tax(base.start, tax_rate, keep_gross=keep_gross),
            flat_tax(base.stop, tax_rate, keep_gross=keep_gross))
    if isinstance(base, CurrencyWithTax):
        if keep_gross:
            new_net = (base.net / fraction).quantize()
            return CurrencyWithTax(net=new_net, gross=base.gross)
        else:
            new_gross = (base.gross * fraction).quantize()
            return CurrencyWithTax(net=base.net, gross=new_gross)
    if isinstance(base, Currency):
        if keep_gross:
            net = (base / fraction).quantize()
            return CurrencyWithTax(net=net, gross=base)
        else:
            gross = (base * fraction).quantize()
            return CurrencyWithTax(net=base, gross=gross)
    raise TypeError('Unknown base for flat_tax: %r' % (base,))
