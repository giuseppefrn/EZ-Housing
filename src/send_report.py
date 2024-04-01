import logging

from .utils.db_queries import get_houses_by_ids


def filter_houses(houses, price=1500):
    """
    Filter the houses with a price less than the given price.
    :param houses: List of houses.
    :param price: Price of the house.
    :return: List of houses.
    """
    filtered_houses = []
    for house in houses:
        if house.get("Rental price", 0) < price:
            filtered_houses.append(house)
    return filtered_houses


def create_report(**kwargs):
    """
    Send an email with the link of the inserted_ids.
    The links are retrieved from the MongoDB database.
    """
    inserted_ids = kwargs.get("ti").xcom_pull(task_ids="load")
    houses = get_houses_by_ids(inserted_ids)
    filtered_houses = filter_houses(houses)

    # Start with an HTML header
    email_content = "<h1>List of new houses:</h1>"

    for house in filtered_houses:
        address = house.get("Address", "No Address")
        price = house.get("Rental price", "No Price")
        link = house.get("link", "#")

        # Use HTML formatting for the link
        email_content += (
            f"<p>House: {address}, "
            f"Price: {price}, "
            f"Link: <a href='{link}'>{link}</a> </p>"
        )

    logging.info(email_content)
    return email_content
