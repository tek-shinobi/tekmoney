from typing import Union
from .currency import Currency
from .currency_range import CurrencyRange
from .currency_tax import CurrencyWithTax

Addable = Union[Currency, CurrencyRange, CurrencyWithTax, "CurrencyRangeTax"]


class CurrencyRangeTax:
    """A taxed money range."""

    __slots__ = ("start", "stop")

    def __init__(self, start: CurrencyWithTax, stop: CurrencyWithTax) -> None:
        if start.currency != stop.currency:
            raise ValueError(
                f"Cannot create a range. {start} and {stop} use different currencies"
            )
        if start > stop:
            raise ValueError(f"Cannot create a range from {start} to {stop}")
        self.start = start
        self.stop = stop

    def __str__(self) -> str:
        return f"CurrencyRangeTax({self.start}, {self.stop})"

    def __add__(self, other: Addable) -> "CurrencyRangeTax":
        if isinstance(other, (Currency, CurrencyWithTax)):
            if other.currency != self.currency:
                raise ValueError(
                    f"Cannot add a range in {self.currency} to argument in {other.currency}"
                )
            start = self.start + other
            stop = self.stop + other
            return CurrencyRangeTax(start, stop)
        elif isinstance(other, (CurrencyRange, CurrencyRangeTax)):
            if other.start.currency != self.currency:
                raise ValueError(
                    f"Cannot add ranges in {self.currency} and {other.currency}"
                )
            start = self.start + other.start
            stop = self.stop + other.stop
            return CurrencyRangeTax(start, stop)
        return NotImplemented

    def __sub__(self, other: Addable) -> "CurrencyRangeTax":
        if isinstance(other, (Currency, CurrencyWithTax)):
            if other.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract argument in {other.currency} from range in {self.currency}"
                )
            start = self.start - other
            stop = self.stop - other
            return CurrencyRangeTax(start, stop)
        elif isinstance(other, (CurrencyRange, CurrencyRangeTax)):
            if other.start.currency != self.start.currency:
                raise ValueError(
                    f"Cannot subtract range in {other.start.currency} from {self.currency}"
                )
            start = self.start - other.start
            stop = self.stop - other.stop
            return CurrencyRangeTax(start, stop)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CurrencyRangeTax):
            return self.start == other.start and self.stop == other.stop
        return False

    def __contains__(self, item: CurrencyWithTax) -> bool:
        if not isinstance(item, CurrencyWithTax):
            raise TypeError(
                f"CurrencyRangeTax requires CurrencyWithTax as left operand, not {type(item)}"
            )
        return self.start <= item <= self.stop

    @property
    def currency(self) -> str:
        """Return the currency of the range."""
        return self.start.currency

    def quantize(self, exp=None, rounding=None) -> "CurrencyRangeTax":
        """Return a copy of the range with start and stop quantized.

        All arguments are passed to `TaxedMoney.quantize` which in turn calls
        `Money.quantize`.
        """
        return CurrencyRangeTax(
            self.start.quantize(exp, rounding=rounding),
            self.stop.quantize(exp, rounding=rounding),
        )

    def replace(
        self, start: CurrencyWithTax = None, stop: CurrencyWithTax = None
    ) -> "CurrencyRangeTax":
        """Return a range with start or stop replaced with given values."""
        if start is None:
            start = self.start
        if stop is None:
            stop = self.stop
        return CurrencyRangeTax(start=start, stop=stop)
