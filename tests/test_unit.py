from pizza_app.services.pricing_service import PricingService


def test_subtotal_calculation(sample_items):
    pricing = PricingService()
    subtotal, discount, total = pricing.totals_from_lines(sample_items)

    assert subtotal == 35.0
    assert discount == 0.0
    assert total == 35.0


def test_discount_applied_above_50():
    pricing = PricingService()
    subtotal, discount, total = pricing.totals_from_lines([60.0])

    assert subtotal == 60.0
    assert discount == 6.0
    assert total == 54.0


def test_no_discount_exactly_50():
    pricing = PricingService()
    subtotal, discount, total = pricing.totals_from_lines([50.0])

    assert subtotal == 50.0
    assert discount == 0.0
    assert total == 50.0