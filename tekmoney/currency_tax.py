import warnings
from decimal import Decimal
from typing import Union

from .currency import Currency

Dint = Union[Decimal, int]
CurrencyAddable = Union[Currency, "CurrencyWithTax"]


class CurrencyWithTax:
    """Stores Currency with net, gross (incl. tax) and tax."""

    __slots__ = ("net", "gross")

    def __init__(self, net: Currency, gross: Currency) -> None:
        if not isinstance(net, Currency) or not isinstance(gross, Currency):
            raise TypeError(f"Price requires Currency, got {net}, {gross}")
        if net.currency != gross.currency:
            raise ValueError(
                f"Different currencies not allowed: {net.currency} and {gross.currency}"
            )
        self.net = net
        self.gross = gross

    def __str__(self) -> str:
        return f"CurrencyWithTax(net={self.net}, gross={self.gross})"

    def __add__(self, other: CurrencyAddable) -> "CurrencyWithTax":
        if isinstance(other, CurrencyWithTax):
            net = self.net + other.net
            gross = self.gross + other.gross
            return CurrencyWithTax(net=net, gross=gross)
        if isinstance(other, Currency):
            net = self.net + other
            gross = self.gross + other
            return CurrencyWithTax(net=net, gross=gross)
        return NotImplemented

    def __sub__(self, other: CurrencyAddable) -> "CurrencyWithTax":
        if isinstance(other, CurrencyWithTax):
            net = self.net - other.net
            gross = self.gross - other.gross
            return CurrencyWithTax(net=net, gross=gross)
        if isinstance(other, Currency):
            net = self.net - other
            gross = self.gross - other
            return CurrencyWithTax(net=net, gross=gross)
        return NotImplemented

    def __lt__(self, other: "CurrencyWithTax") -> bool:
        if isinstance(other, CurrencyWithTax):
            return self.gross < other.gross
        elif isinstance(other, Currency):
            raise TypeError(
                "Cannot compare taxed and untaxed Currency,"
                " use currency_with_tax.net or currency_with_tax.gross explicitly"
            )
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CurrencyWithTax):
            return self.gross == other.gross and self.net == other.net
        return False

    def __le__(self, other: "CurrencyWithTax") -> bool:
        if self == other:
            return True
        return self < other

    def __mul__(self, other: Dint) -> "CurrencyWithTax":
        try:
            net = self.net * other
            gross = self.gross * other
        except TypeError:
            return NotImplemented
        return CurrencyWithTax(net=net, gross=gross)

    def __rmul__(self, other: Dint) -> "CurrencyWithTax":
        return self * other

    def __truediv__(self, other: Dint) -> "CurrencyWithTax":
        try:
            net = self.net / other
            gross = self.gross / other
        except TypeError:
            return NotImplemented
        return CurrencyWithTax(net=net, gross=gross)

    def __bool__(self) -> bool:  # pragma: no cover
        warnings.warn(
            RuntimeWarning(
                "`bool(currency_with_tax)` will always evaluate to True, consider"
                " replacing the test with explicit `if currency_with_tax is None`"
                " or `if currency_with_tax.gross`."
            ),
            stacklevel=2,
        )
        return True

    @property
    def currency(self) -> str:
        """Return the currency-unit of the currency. Like 'USD'."""
        return self.net.currency

    @property
    def tax(self) -> Currency:
        """Return the tax amount."""
        return self.gross - self.net

    def quantize(self, exp=None, rounding=None) -> "CurrencyWithTax":
        """Return a new instance with both net and gross quantized.

        All arguments are passed to `Currency.quantize`.
        """
        return CurrencyWithTax(
            net=self.net.quantize(exp, rounding=rounding),
            gross=self.gross.quantize(exp, rounding=rounding),
        )
