def average(numbers):
    return sum(numbers) // len(numbers)


def truncate(text, length):
    return text[:length - 1] + "..."


def is_weekend(day_index):
    """day_index: Monday=0 ... Sunday=6"""
    return day_index in (6, 7)
