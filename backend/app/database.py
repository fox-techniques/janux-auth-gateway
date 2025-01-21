from pymongo import MongoClient

# MongoDB connection URI
MONGO_URI = "mongodb://localhost:27017"  # Docker exposes this on localhost

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["janux_db"]

# Collections
users_collection = db["users"]
