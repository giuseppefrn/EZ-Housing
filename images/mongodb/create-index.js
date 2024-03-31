// Switch to the desired database
db = db.getSiblingDB('housing');

// Create a unique index on the 'link' field of the 'houses' collection
db.houses.createIndex({"link": 1}, {unique: true});

// Create a TTL index on the 'expires_at' field of the 'houses' collection
// Set expireAfterSeconds to 0 to indicate that documents should expire at the time specified in the 'expires_at' field
db.houses.createIndex({"expires_at": 1}, {expireAfterSeconds: 0});
