import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from .utils.general import (
    get_city_name_from_pararius,
    get_houses_from_pararius,
    get_info_from_pararius,
)


def extract_data(
    link: str = "https://www.pararius.com/apartments/leiden/600-1500/radius-25/since-1",  # noqa
    output_dir: str = "outputs/extracted",
):
    """
    Extracts data from the Pararius website and saves it as a csv file.
    :param link:
    :param output_dir:
    :return:
    """

    # get the root folder of the project
    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Setting output_dir
    abs_output_dir = os.path.join(root_folder, output_dir)

    # Setting up Firefox options to run headless
    options = Options()
    options.headless = True

    # Explicitly specify the path to geckodriver
    service = Service(executable_path="/usr/local/bin/geckodriver")

    # Opening the driver with the configured options
    driver = webdriver.Firefox(service=service, options=options)

    # getting the list of houses (links)
    houses_list = get_houses_from_pararius(link, driver)

    print(houses_list)

    if not houses_list:
        raise ValueError("No houses found. The list is empty.")

    # inizialize the dataframe
    df = pd.DataFrame(houses_list, columns=["link"])

    # adding city name to df
    df["city"] = df["link"].apply(get_city_name_from_pararius)

    # populating the dataframe
    for i, row in df.iterrows():
        link = row["link"]
        res = get_info_from_pararius(link, driver)
        df.loc[i, res.keys()] = res.values()

    # closing the driver
    driver.close()

    # writing the dataframe as csv
    os.makedirs(abs_output_dir, exist_ok=True)
    df.to_csv(os.path.join(abs_output_dir, "houses-info.csv"), index=False)


if __name__ == "__main__":
    extract_data()
