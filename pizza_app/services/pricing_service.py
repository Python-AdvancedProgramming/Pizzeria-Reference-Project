"""Pricing rules.

User story:
- 10% discount is applied automatically if the sum exceeds 50 CHF.
"""

from __future__ import annotations

from typing import Iterable, Tuple


class PricingService:
    """Pricing and discount calculations."""

    def __init__(self, discount_threshold_chf: float = 50.0, discount_rate: float = 0.10) -> None:
        self.discount_threshold_chf = discount_threshold_chf
        self.discount_rate = discount_rate

    def totals_from_lines(self, line_totals: Iterable[float]) -> Tuple[float, float, float]:
        """Compute subtotal, discount, total from line totals.

        Args:
            line_totals: Each line's total price (already quantity * unit price)

        Returns:
            (subtotal, discount, total)
        """
        subtotal = round(sum(line_totals), 2)
        discount = round(subtotal * self.discount_rate, 2) if subtotal > self.discount_threshold_chf else 0.0
        total = round(subtotal - discount, 2)
        return subtotal, discount, total
