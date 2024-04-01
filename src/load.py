import datetime
import os

import pandas as pd
from pymongo import errors

from .utils.db_queries import get_collection


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

    collection = get_collection()
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

    return [str(obj_id) for obj_id in inserted_ids]


if __name__ == "__main__":
    load_data()
