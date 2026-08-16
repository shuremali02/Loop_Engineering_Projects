def get_user(user_id):
    # TODO: validate user_id before querying the database
    return {"id": user_id, "name": "placeholder"}


def send_email(to, subject, body):
    # TODO: add retry logic if the SMTP server times out
    print(f"Sending email to {to}: {subject}")


def calculate_total(items):
    # TODO: apply discount codes before summing the total
    return sum(item["price"] for item in items)
