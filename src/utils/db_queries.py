import os

from bson.objectid import ObjectId
from pymongo import MongoClient


def get_collection():
    """
    Get the collection object from the MongoDB database.
    :return: collection object
    """
    user = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
    password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")

    client = MongoClient(f"mongodb://{user}:{password}@mongodb:27017")
    db = client.housing
    collection = db.houses
    return collection


def get_houses():
    """
    Get all the houses from the database.
    :return: List of houses.
    """
    collection = get_collection()
    houses = []
    for house in collection.find():
        houses.append(house)
    return houses


def get_houses_with_price_greater_than(price):
    """
    Get all the houses with a price greater than the given price.
    :param price: Price of the house.
    :return: List of houses.
    """
    collection = get_collection()
    houses = []
    for house in collection.find({"Rental price": {"$gt": price}}):
        houses.append(house)
    return houses


def get_houses_with_price_less_than(price):
    """
    Get all the houses with a price less than the given price.
    :param price: Price of the house.
    :return: List of houses.
    """
    collection = get_collection()
    houses = []
    for house in collection.find({"Rental price": {"$lt": price}}):
        houses.append(house)
    return houses


def get_houses_by_ids(inserted_ids):
    """
    Get the houses by the given ids.
    :param inserted_ids: List of ids.
    :return: List of houses.
    """
    collection = get_collection()
    inserted_ids = [ObjectId(id_) for id_ in inserted_ids]
    houses = []
    for house in collection.find({"_id": {"$in": inserted_ids}}):
        houses.append(house)
    return houses


def insert_house(house):
    """
    Insert a house into the database.
    :param house: House object.
    :return: Inserted id.
    """
    collection = get_collection()
    result = collection.insert_one(house)
    return str(result.inserted_id)


def empty_collection():
    """
    Empty the collection.
    """
    collection = get_collection()
    collection.delete_many({})


if __name__ == "__main__":
    print(get_houses())

    # empty the collection
    empty_collection()

    print(get_houses())
