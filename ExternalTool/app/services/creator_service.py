
from pymongo import MongoClient, ASCENDING
import os
from app.utils.generator import create_user

mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/db_creators')
client = MongoClient(mongo_uri)
db = client.get_default_database()
collection = db.resume_creators_info

SIZE_MAP = {
    'small': 500,
    'medium': 5000,
    'large': 10000
}

def generate_creators(size: str) -> int:
    quantity = SIZE_MAP.get(size)
    if not quantity:
        raise ValueError("Invalid size")
    users = [create_user() for _ in range(quantity)]
    collection.insert_many(users)
    return quantity

def list_creators(page: int = 1, per_page: int = 100):
    skip = (page - 1) * per_page
    cursor = collection.find({}, {'_id': 0}).skip(skip).limit(per_page)
    return list(cursor)

def delete_all_creators():
    result = collection.delete_many({})
    return result.deleted_count

def create_indexes():
    indexes = []
    indexes.append(collection.create_index([("createdAt", ASCENDING), ("clientId", ASCENDING)], name="idx_createdAt_clientId"))
    indexes.append(collection.create_index([("updatedAt", ASCENDING), ("clientId", ASCENDING)], name="idx_updatedAt_clientId"))
    indexes.append(collection.create_index([("contentType", ASCENDING), ("createdAt", ASCENDING)], name="idx_contentType_createdAt"))
    return indexes
