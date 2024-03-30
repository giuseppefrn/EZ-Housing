import argparse
import os

import pandas as pd
from selenium import webdriver

from utils.general import (
    get_city_name_from_pararius,
    get_houses_from_pararius,
    get_info_from_pararius,
)

if __name__ == "__main__":
    print()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--link",
        type=str,
        default="https://www.pararius.com/apartments/leiden/700-1500/since-1",
        help="Link to start your search. i.e. "
        "https://www.pararius.com/apartments/utrecht",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="outputs/extracted",
        help="path to the output folder",  # noqa
    )

    opt = parser.parse_args()

    # opening the driver
    driver = webdriver.Firefox()

    # getting the list of houses (links)
    houses_list = get_houses_from_pararius(opt.link, driver)

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
    os.makedirs(opt.output_dir, exist_ok=True)
    df.to_csv(os.path.join(opt.output_dir, "houses-info.csv"), index=False)
