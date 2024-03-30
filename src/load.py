# load the data into mongodb

import pandas as pd
from pymongo import MongoClient

if __name__ == "__main__":
    # Load the transformed data
    houses_info_df = pd.read_csv(
        "outputs/transformed/houses-info-transformed.csv"
    )  # noqa

    # Connect to the database
    client = MongoClient(
        "mongodb://root:example@localhost:27017/"
    )  # todo change password using env variables or secrets
    db = client["housing"]
    collection = db["houses"]

    # Insert the data into the database
    collection.insert_many(houses_info_df.to_dict(orient="records"))

    print("Data loaded into MongoDB successfully.")
