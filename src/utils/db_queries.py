from bson.objectid import ObjectId
from pymongo import MongoClient


def get_collection():
    """
    Get the collection object from the MongoDB database.
    :return: collection object
    """
    client = MongoClient(
        "mongodb://root:example@mongodb:27017"
    )  # todo change password using env variables or secrets
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
