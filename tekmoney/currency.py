from typing import Union
from decimal import Decimal
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
        self.amount = amount
        self.currency = currency.upper() or 'USD'

    def __str__(self) -> str:
        return f'{str(self.amount)} {self.currency}'
