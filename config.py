# core/database/mongodb_handler.py
from pymongo import MongoClient
from core.config import Config

class MongoDBHandler:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_URI)
        self.db = self.client['ai_database']
        
    def store_conversation(self, data):
        return self.db.conversations.insert_one(data)
        
    def store_learning(self, data):
        return self.db.learned_data.insert_one(data)
        
    def get_relevant_context(self, query):
        return self.db.conversations.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(5)
