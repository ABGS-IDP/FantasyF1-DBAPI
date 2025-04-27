from pymongo import MongoClient

class MongoDBClient:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection_name: str, document: dict):
        result = self.db[collection_name].insert_one(document)
        document["_id"] = result.inserted_id
        return document

    def find_all(self, collection_name: str):
        return list(self.db[collection_name].find())
