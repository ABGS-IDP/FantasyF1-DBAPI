from pymongo import MongoClient, ASCENDING
from typing import Optional

class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

        self.db.users.create_index([("username", ASCENDING)], unique=True)
        self.db.users.create_index([("email", ASCENDING)], unique=True)
        self.db.drivers.create_index([("name", ASCENDING)], unique=True)
        self.db.drivers.create_index([("team", ASCENDING)])
        self.db.teams.create_index([("name", ASCENDING)], unique=True)


    def insert_one(self, collection_name: str, document: dict):
        result = self.db[collection_name].insert_one(document)
        document["_id"] = result.inserted_id
        return document
    

    def find(self, collection_name: str, query: Optional[dict] = {}):
        return list(self.db[collection_name].find(query))


    def find_one(self, collection_name: str, query: dict):
        return self.db[collection_name].find_one(query)


    def update_one(self, collection_name: str, query: dict, update: dict):
        result = self.db[collection_name].update_one(query, {"$set": update})
        return result.modified_count


    def delete(self, collection_name: str, query: dict = {}):
        result = self.db[collection_name].delete_many(query)
        return result.deleted_count
