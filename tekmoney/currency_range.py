from typing import Union
from .currency import Currency

Addable = Union["CurrencyRange", Currency]


class CurrencyRange:
    """Taxable currency range"""

    __slots__ = ("start", "stop")

    def __init__(self, start: Currency, stop: Currency) -> None:
        if not isinstance(start, Currency) and not isinstance(stop, Currency):
            raise TypeError(
                f"Currency Range start and stop need to be of type Currency"
            )
        if start.currency != stop.currency:
            raise ValueError(
                f"Cannot create range for different currencies. start:{start.currency} stop:{stop.currency}"
            )
        if start > stop:
            raise ValueError(
                f"Cannot create a range from {start.amount} to {stop.amount}"
            )
        self.start = start
        self.stop = stop

    def __str__(self) -> str:
        return f"CurrencyRange({self.start} {self.stop})"

    @property
    def currency(self) -> str:
        """ return the currency denomination. Like USD or EUR """
        return self.start.currency

    def __add__(self, other: Addable) -> "CurrencyRange":
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f"cannot add ranges in {self.currency} and {other.currency}"
                )
            start = self.start + other
            stop = self.stop + other
            return CurrencyRange(start, stop)
        elif isinstance(other, CurrencyRange):
            if other.start.currency != self.currency:
                raise ValueError(
                    f"cannot add ranges in {self.currency} and {other.start.currency}"
                )
            start = self.start + other.start
            stop = self.stop + other.stop
            return CurrencyRange(start, stop)
        return NotImplemented

    def __sub__(self, other: Addable) -> "CurrencyRange":
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f"cannot add ranges in {self.currency} and {other.currency}"
                )
            start = self.start - other
            stop = self.stop - other
            return CurrencyRange(start, stop)
        elif isinstance(other, CurrencyRange):
            if other.start.currency != self.currency:
                raise ValueError(
                    f"cannot add ranges in {self.currency} and {other.start.currency}"
                )
            start = self.start - other.start
            stop = self.stop - other.stop
            return CurrencyRange(start, stop)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CurrencyRange):
            return self.start == other.start and self.stop == other.stop
        return False

    def __contains__(self, item: Currency) -> bool:
        if not isinstance(item, Currency):
            raise TypeError(
                f"currency_range requires currency as left operand, not {type(item)}"
            )
        return self.start <= item <= self.stop

    def quantize(self, exp=None, rounding=None) -> "CurrencyRange":
        """Return a copy of the range with start and stop quantized.

        All arguments are passed to 'Currency.quantize'.
        """
        return CurrencyRange(
            self.start.quantize(exp, rounding=rounding),
            self.stop.quantize(exp, rounding=rounding),
        )

    def replace(self, start: Currency = None, stop: Currency = None) -> "CurrencyRange":
        """Return a range with start or stop replaced with given values."""
        if start is None:
            start = self.start
        if stop is None:
            stop = self.stop
        return CurrencyRange(start=start, stop=stop)
