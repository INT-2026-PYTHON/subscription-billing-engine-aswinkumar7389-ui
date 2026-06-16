"""
VATCalculator — single-rate VAT (e.g. 19% in Germany).
"""

from decimal import Decimal

from billing_engine.money import Money
from billing_engine.taxes.base import TaxCalculator, TaxContext, TaxBreakdown


class VATCalculator(TaxCalculator):
    def __init__(self, rate: Decimal) -> None:
        # TODO Day 1
        # Reject float
        if isinstance(rate, float):
            raise TypeError("rate must be a Decimal, not float")
        # Validate range
        if not (Decimal("0") <= rate <= Decimal("1")):
            raise ValueError("rate must be between 0 and 1")
        self.rate = rate

    def apply(self, taxable: Money, context: TaxContext) -> TaxBreakdown:
        # TODO Day 1
        # Calculate VAT
        vat = taxable * self.rate

        # Format percentage cleanly
        pct = self.rate * Decimal(100)
        label = f"VAT {pct}%"

        return TaxBreakdown(
            components=[(label, vat)],
            total=vat
        )