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

    def update_one(self, collection_name: str, query: dict, update: dict):
        result = self.db[collection_name].update_one(query, {"$set": update})
        return result.modified_count

    def find_one(self, collection_name: str, query: dict):
        return self.db[collection_name].find_one(query)

    def delete_all_by_query(self, collection_name: str, query: dict):
        result = self.db[collection_name].delete_many(query)
        return result.deleted_count

    def delete_all(self, collection_name: str):
        result = self.db[collection_name].delete_many({})
        return result.deleted_count
