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
    The links are retreived from the MongoDB database.
    """
    inserted_ids = kwargs.get("ti").xcom_pull(task_ids="load")
    houses = get_houses_by_ids(inserted_ids)
    filtered_houses = filter_houses(houses)

    email_content = "List of new houses:\n\n"

    for house in filtered_houses:
        email_content += (
            f"House: {house.get('Address')}, "
            f"Price: {house.get('Rental price')}, "
            f"Link: {house.get('link')} \n"
        )
    return email_content
