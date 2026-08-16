"""Shipping cost calculator for the doorbell-loop sample repo."""


def calculate_shipping_cost(weight, discount=None):
    base_cost = weight * 5
    if discount is None:
        discount = 0
    return base_cost - discount


def apply_bulk_rate(item_count, rate=None):
    if rate is None:
        rate = 1
    return item_count * rate
