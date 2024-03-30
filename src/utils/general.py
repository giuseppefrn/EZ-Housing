import time

from bs4 import BeautifulSoup


# get the city name from the link
# for pararius it is the -3 element splitted by /
def get_city_name_from_pararius(link):
    return link.split("/")[-3]


# get the list of house from pararius link
def get_houses_from_pararius(link, driver):
    try:
        houses_list = []
        driver.get(link)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html)

        results = soup.find_all(
            class_="listing-search-item__link "
            "listing-search-item__link--depiction"  # noqa
        )

        for item in results:
            line = item.get("href")
            line = "https://www.pararius.com" + line
            houses_list.append(line)
        return houses_list
    except Exception:
        return 0


# Core function for pararius return the information from the link
def get_info_from_pararius(link, driver):
    price, number, agent = -1, -1, None

    print("Starting", link)
    try:
        driver.get(link)
        # print('got page')
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html)
    except Exception as e:
        print("Driver error", e)
        return price, number, agent

    results = soup.find(class_="listing-detail-summary__price")
    if results:
        price = results.text
        price = price.split("\n")[-4]
        price = price.split("€")[-1]
        price = price.replace(",", "")
    else:
        print("Price error")

    results = soup.find(
        class_="agent-summary__link agent-summary__link--hidden agent-summary__link--call-agent"  # noqa
    )
    if results:
        number = results.text
        number = "+" + number.split("\n")[-2].split("+")[-1]
    else:
        print("Number error")

    results = soup.find(class_="agent-summary__title-link")
    if results:
        agent = results.text
    else:
        print("Agent error")

    values = soup.find_all(class_="listing-features__main-description")
    keys = soup.find_all(class_="listing-features__term")

    res = {}
    for key, value in zip(keys, values):
        res[key.text] = value.text

    res["price"] = price
    res["number"] = number
    res["agent"] = agent

    return res
