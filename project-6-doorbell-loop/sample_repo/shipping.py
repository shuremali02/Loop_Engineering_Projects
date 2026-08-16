"""Shipping cost calculator for the doorbell-loop sample repo."""


def calculate_shipping_cost(weight, discount=None):
    base_cost = weight * 5
    return base_cost - discount


def apply_bulk_rate(item_count, rate=None):
    return item_count * rate
