import threading
import pymongo
from info import DATABASE_URI, DATABASE_NAME

# MongoDB connection setup
myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
parentid_collection = mydb['parentid']

# Thread lock for safe concurrent access
INSERTION_LOCK = threading.RLock()

def search_parent(chat_id):
    with INSERTION_LOCK:
        try:
            document = parentid_collection.find_one({"chat_id": chat_id})
            if document:
                return document.get("parent_id", 'root')
            else:
                return 'root'
        except Exception as e:
            print(f"Error searching for parent ID: {e}")
            return 'root'

def _set(chat_id, parent_id):
    with INSERTION_LOCK:
        try:
            parentid_collection.update_one(
                {"chat_id": chat_id},
                {"$set": {"parent_id": parent_id}},
                upsert=True
            )
        except Exception as e:
            print(f"Error setting parent ID: {e}")

def _clear(chat_id):
    with INSERTION_LOCK:
        try:
            parentid_collection.delete_one({"chat_id": chat_id})
        except Exception as e:
            print(f"Error clearing parent ID: {e}")

# Example usage
def set_parent(chat_id, parent_id):
    _set(chat_id, parent_id)

def get_parent(chat_id):
    return search_parent(chat_id)

def clear_parent(chat_id):
    _clear(chat_id)
