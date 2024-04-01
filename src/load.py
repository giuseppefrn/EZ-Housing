import datetime
import os

import pandas as pd
from pymongo import MongoClient, errors


def load_data():
    """
    Load the data into the MongoDB database.
    :return:
    """

    root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    houses_info_df = pd.read_csv(
        os.path.join(
            root_folder, "outputs/transformed/houses-info-transformed.csv"
        )  # noqa
    )

    client = MongoClient(
        "mongodb://root:example@mongodb:27017/"
    )  # todo change password using env variables or secrets
    db = client["housing"]
    collection = db["houses"]
    houses_info_df["load_date"] = datetime.datetime.now()
    houses_info_df["expires_at"] = datetime.datetime.now() + datetime.timedelta(  # noqa
        days=30
    )

    documents = houses_info_df.to_dict(orient="records")

    inserted_ids = []

    for doc in documents:
        # insert document into collection
        try:
            result = collection.insert_one(doc)
            print(f"Inserted document with id: {result.inserted_id}")
            inserted_ids.append(result.inserted_id)

        except errors.DuplicateKeyError as dke:
            # Log or handle the details of the duplicate error as needed
            print("Document is a duplicate and not inserted.")

            # Example: Printing the error details
            print(f"Error details: {dke.details}")

        except errors.BulkWriteError as bwe:
            # Log or handle the details of the bulk write error as needed
            print("Bulk write error occurred.")
            # Example: Printing the error details
            print(f"Error details: {bwe.details}")

    return inserted_ids


if __name__ == "__main__":
    load_data()
