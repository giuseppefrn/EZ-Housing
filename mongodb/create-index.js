// Switch to the desired database
db = db.getSiblingDB('housing');

// Create a unique index on the 'link' field of the 'houses' collection
db.houses.createIndex({"link": 1}, {unique: true});
