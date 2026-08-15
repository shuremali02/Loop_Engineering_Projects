def format_currency(amount):
    return f"${amount:.2f}"


def parse_config(path):
    # TODO: handle missing config file gracefully instead of crashing
    with open(path) as f:
        return f.read()
