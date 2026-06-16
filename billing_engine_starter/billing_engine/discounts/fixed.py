"""
FixedAmountDiscount — e.g., flat ₹500 off.

CAPPING RULE: if the fixed amount exceeds the subtotal, return subtotal
(so the discounted total never goes below zero).
"""

from billing_engine.money import Money
from billing_engine.discounts.base import Discount, DiscountContext


class FixedAmountDiscount(Discount):
    def __init__(self, amount: Money) -> None:
        # Defensive check: ensure non-negative
        if amount < Money.zero(amount.currency):
            raise ValueError("amount must be non-negative")

        self.amount = amount

    def apply(self, subtotal: Money, context: DiscountContext) -> Money:
        # Validate currency match
        if self.amount.currency != subtotal.currency:
            raise ValueError("currency mismatch between amount and subtotal")

        # Return the smaller of subtotal or discount amount
        return min(self.amount, subtotal)
