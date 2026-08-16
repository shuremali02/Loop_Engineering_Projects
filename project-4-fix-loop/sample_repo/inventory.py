def apply_discount(price, percent):
    """Apply a percent discount to a price."""
    return price - (price * percent / 100)


def restock(current_stock, incoming):
    return current_stock + incoming


def days_of_stock_left(current_stock, daily_usage):
    """How many full days of stock remain at the current daily usage."""
    return current_stock / daily_usage
