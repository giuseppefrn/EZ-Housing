import logging

from .utils.db_queries import get_houses_by_ids


def filter_houses(houses, price=1700):
    """
    Filter the houses with a price less than the given price.
    :param houses: List of houses.
    :param price: Price of the house.
    :return: List of houses.
    """
    filtered_houses = []
    for house in houses:
        if (
            house.get("Rental price", 0) < price
            and house.get("Living area", 100) >= 45  # noqa
        ):
            filtered_houses.append(house)
    return filtered_houses


def prepare_slack_report(**kwargs):
    """
    Send slack report with the link of the inserted_ids.
    The links are retrieved from the MongoDB database.
    """
    inserted_ids = kwargs.get("ti").xcom_pull(task_ids="load")
    houses = get_houses_by_ids(inserted_ids)
    filtered_houses = filter_houses(houses)

    if not filtered_houses:
        logging.info("No houses found with the given price.")
        return None

    # Start with an HTML header
    slack_content = "*List of new houses:*\n"

    for house in filtered_houses:
        title = house.get("title")
        price = house.get("Rental price", "No Price")
        link = house.get("link", "#")

        # Use Slack Mrkdwn formatting
        slack_content += f"*{title}*\n"
        slack_content += f"<{link}|View House>\n"  # Slack format for links
        slack_content += f"Price: {price}\n\n"  # Adding a new line for spacing

    logging.info(slack_content)
    return slack_content


def prepare_telegram_report(**kwargs):
    """
    Prepare a Telegram report with the links of the inserted_ids.
    The links are retrieved from the MongoDB database.
    """
    inserted_ids = kwargs.get("ti").xcom_pull(task_ids="load")
    houses = get_houses_by_ids(inserted_ids)
    filtered_houses = filter_houses(houses)

    if not filtered_houses:
        logging.info("No houses found with the given criteria.")
        return None

    # Start with a Markdown header
    telegram_content = "🏘 *List of new houses:* 🏘\n\n"

    for house in filtered_houses:
        title = house.get("title")
        price = house.get("Rental price", "No Price")
        link = house.get("link", "#")
        living_area = house.get("Living area", "Unknown")

        # Use Telegram Markdown formatting
        telegram_content += f"🏡 *{title}*\n"
        telegram_content += f"[View House]({link})\n"
        telegram_content += f"_Price: {price}_\n".replace(".", "\\.")
        telegram_content += f"_Living area: {living_area}_\n\n".replace(
            ".", "\\."
        )  # noqa

    logging.info(telegram_content)
    return telegram_content


def prepare_email_report(**kwargs):
    """
    Send an email with the link of the inserted_ids.
    The links are retrieved from the MongoDB database.
    """
    inserted_ids = kwargs.get("ti").xcom_pull(task_ids="load")
    houses = get_houses_by_ids(inserted_ids)
    filtered_houses = filter_houses(houses)

    if not filtered_houses:
        logging.info("No houses found with the given price.")
        return None

    # Start with an HTML header
    email_content = "<h1>List of new houses:</h1>"

    for house in filtered_houses:
        title = house.get("title")
        price = house.get("Rental price", "No Price")
        link = house.get("link", "#")

        # Use HTML formatting for the link
        email_content += f"<p><strong>{title}</strong></p>"
        email_content += f"<p><a href='{link}'>{link}</a></p>"
        email_content += f"<p>Price: {price}</p>"
        email_content += "<br>"

    logging.info(email_content)
    return email_content
