"""
Proration — Day 4 stretch.

Mid-cycle plan change: customer is on Plan A from period_start to period_end,
but on `switch_date` they upgrade (or downgrade) to Plan B.

Day-count proration:
    total_days     = (period_end - period_start).days
    used_days      = (switch_date - period_start).days
    remaining_days = total_days - used_days

    credit = old_price * (remaining_days / total_days)
    charge = new_price * (remaining_days / total_days)

Tax MUST be recalculated on BOTH legs (reverse-tax on the credit,
fresh tax on the new charge). Tax is NOT prorated linearly — the tax
on a proration credit/charge is just `tax_calc.apply(credit_or_charge)`.

The two legs are returned as TAX-INCLUSIVE Money values for the
PRORATION_CREDIT (negative) and PRORATION_CHARGE (positive) line items.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from billing_engine.money import Money
from billing_engine.taxes.base import TaxCalculator, TaxContext


@dataclass(frozen=True)
class ProrationResult:
    credit_amount: Money     # always returned as a POSITIVE Money; caller negates for line item
    charge_amount: Money     # always positive
    credit_tax: Money        # tax that was on the credit
    charge_tax: Money        # tax that is on the new charge


def compute_proration(
    old_plan_price: Money,
    new_plan_price: Money,
    period_start: date,
    period_end: date,
    switch_date: date,
    tax_calc: TaxCalculator,
    tax_context: TaxContext,
) -> ProrationResult:
    """Pure function. STRETCH — implement only after Days 1+2 are green."""
    # TODO Day 4
    def compute_proration(
    old_plan_price: Money,
    new_plan_price: Money,
    period_start: date,
    period_end: date,
    switch_date: date,
    tax_calc: TaxCalculator,
    tax_context: TaxContext,
) -> ProrationResult:
     """Calculates prorated charges and credits for a mid-cycle plan change."""
    
   # 1. Validation Checks
    if old_plan_price.currency != new_plan_price.currency:
        raise ValueError("Currency mismatch between old plan and new plan prices.")
        
    if switch_date < period_start or switch_date > period_end:
        raise ValueError("Switch date must be within the bounds of the billing period.")

    # 2. Day-Count Proration Math
    total_days = (period_end - period_start).days
    used_days = (switch_date - period_start).days
    remaining_days = total_days - used_days

    if total_days <= 0:
        ratio = Decimal("0")
    else:
        ratio = Decimal(remaining_days) / Decimal(total_days)

    # 3. Calculate Base Amounts
    old_val = Decimal(str(old_plan_price.amount))
    new_val = Decimal(str(new_plan_price.amount))
    
    # Round the base prorated amounts
    credit_val = (old_val * ratio).quantize(Decimal('0.01'))
    charge_val = (new_val * ratio).quantize(Decimal('0.01'))

    MoneyClass = type(old_plan_price)
    credit_amount = MoneyClass(credit_val, old_plan_price.currency)
    charge_amount = MoneyClass(charge_val, new_plan_price.currency)

    # 4. Calculate Tax on Both Legs
    credit_breakdown = tax_calc.apply(credit_amount, tax_context)
    charge_breakdown = tax_calc.apply(charge_amount, tax_context)

    # 5. Round the Tax Amounts! (Fixes the 92.9034 bug)
    credit_tax_val = Decimal(str(credit_breakdown.total.amount)).quantize(Decimal('0.01'))
    charge_tax_val = Decimal(str(charge_breakdown.total.amount)).quantize(Decimal('0.01'))
    
    credit_tax = MoneyClass(credit_tax_val, credit_amount.currency)
    charge_tax = MoneyClass(charge_tax_val, charge_amount.currency)

    # 6. Return the Results
    return ProrationResult(
        credit_amount=credit_amount,
        charge_amount=charge_amount,
        credit_tax=credit_tax,
        charge_tax=charge_tax
    )
