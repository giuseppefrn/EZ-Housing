from pymongo import MongoClient

client = MongoClient(
    "mongodb://root:example@localhost:27017"
)  # todo change password using env variables or secrets
db = client.housing
collection = db.houses

for house in collection.find():
    print(house)

print("houses with price greater than 1000")
for house in collection.find({"Rental price": {"$gt": 500}}):
    print(house)
