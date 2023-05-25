import pandas as pd
from selenium import webdriver

import os
import argparse

from utils.general import *

if __name__ == "__main__":
    print()

    parser = argparse.ArgumentParser()
    #TODO add others illuminants
    parser.add_argument('--link', type=str, required=True, help='Link to start your search. i.e. https://www.pararius.com/apartments/utrecht')
    parser.add_argument('--output_dir', type=str, default='outputs', help='path to the output folder')

    opt = parser.parse_args()

    #opening the driver
    driver = webdriver.Firefox()

    #getting the list of houses (links)
    houses_list = get_houses_from_pararius(opt.link, driver)

    #inizialize the dataframe
    df = pd.DataFrame(houses_list, columns=["link"])

    #adding city name to df
    df['city'] = df['link'].apply(get_city_name_from_pararius)

    #populating the dataframe
    for i, row in df.iterrows():
        link = row['link']
        res = get_info_from_pararius(link)
        df.loc[i, res.keys()] = res.values()    

    #writing the dataframe as csv
    os.makedirs(opt.output_dir, exist_ok=True)
    df.to_csv(os.path.join(opt.output_dir, "houses-info.csv"))