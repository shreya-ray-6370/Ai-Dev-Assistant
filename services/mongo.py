from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

import os
import uuid

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["ai_dev_assistant"]

collection = db["messages"]


def create_session():
    return str(uuid.uuid4())


def save_message(username, session_id, role, content):
    collection.insert_one({
        "username": username,
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })


def load_messages(username, session_id):
    return list(
        collection.find(
            {"username": username, "session_id": session_id},
            {"_id": 0}
        ).sort("timestamp", 1)
    )


def get_sessions(username):
    return list(collection.aggregate([

        {"$match": {"username": username}},

        {"$sort": {"timestamp": 1}},

        {
            "$group": {
                "_id": "$session_id",
                "first_message": {"$first": "$content"},
                "last_time": {"$last": "$timestamp"}
            }
        },

        {"$sort": {"last_time": -1}}

    ]))