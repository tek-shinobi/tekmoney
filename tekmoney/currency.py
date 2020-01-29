from typing import Union, overload
from decimal import Decimal, ROUND_HALF_UP
from babel.numbers import get_currency_precision
import warnings

Dint = Union[Decimal, int]


class Currency:
    """Handles money per specified currency"""

    __slots__ = ('amount', 'currency')

    def __init__(self, amount: Dint, currency: str) -> None:
        if isinstance(amount, float):
            warnings.warn(
                SyntaxWarning(  # pragma: no cover
                    'float value detected. Please use Decimal instead.'
                ),
                stacklevel=2
            )
        self.amount = Decimal(amount)
        self.currency = currency.upper() or 'USD'

    def __str__(self) -> str:
        return f'{str(self.amount)} {self.currency}'

    def __bool__(self) -> bool:
        return bool(self.amount)

    @overload
    def __truediv__(self, other: Dint) -> 'Currency':
        ...  # no pragma cover

    @overload
    def __truediv__(self, other: 'Currency') -> 'Dint':
        ...  # no pragma cover

    def __truediv__(self, other):
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f'cannot div {self.currency} from {other.currency}'
                )
            return self.amount / other.amount
        try:
            amount = self.amount / other
        except TypeError:
            return NotImplemented
        return Currency(
            amount,
            self.currency
        )

    def __add__(self, other: 'Currency') -> 'Currency':
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f'cannot add {self.currency} to {other.currency}'
                )
            return Currency(
                self.amount + other.amount,
                self.currency
            )
        return NotImplemented

    def __sub__(self, other: 'Currency') -> 'Currency':
        """negative currency situation needs to be handled externally"""
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f'cannot subtract {self.currency} from {other.currency}'
                )
            amount = self.amount - other.amount
            return Currency(
                amount,
                self.currency
            )
        return NotImplemented

    def __mul__(self, other: Dint) -> 'Currency':
        try:
            amount = self.amount * other
        except TypeError:
            return NotImplemented
        return Currency(amount, self.currency)

    def __rmul__(self, other: Dint) -> 'Currency':
        return self * other

    def __lt__(self, other: 'Currency') -> bool:
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f'cannot compare {self.currency} with {other.currency}'
                )
            return self.amount < other.amount
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Currency):
            return (
                    self.amount == other.amount and
                    self.currency == other.currency)
        return False

    def __gt__(self, other: 'Currency') -> bool:
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise ValueError(
                    f'cannot compare {self.currency} with {other.currency}'
                )
            return self.amount > other.amount
        return NotImplemented

    def __le__(self, other: 'Currency') -> bool:
        if self == other:
            return True
        return self < other

    def __ge__(self, other: 'Currency') -> bool:
        if self == other:
            return True
        return self > other

    def quantize(self, exp=None, rounding=None) -> 'Currency':
        """
        :param exp: fractional part of currency. Like cents in dollar. It can be set to any arbitrary amount.
        :param rounding: ROUND_DOWN, ROUND_UP, ROUND_HALF_UP
        :return: Currency object
        The quantize() method rounds a number to a fixed exponent.
        This method is useful for monetary applications that
        often round results to a fixed number of places
        Example: (10.001, 'USD').quantize(exp='.01', rounding=ROUND_DOWN)
        results in (10.00, 'USD')
        """
        if exp is None:
            exp = Decimal('0.1') ** get_currency_precision(self.currency)
        else:
            exp = Decimal(exp)
        if rounding is None:
            rounding = ROUND_HALF_UP
        return Currency(
            self.amount.quantize(exp=exp, rounding=rounding),
            self.currency
        )


