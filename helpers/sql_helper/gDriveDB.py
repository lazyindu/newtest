import pickle
import threading
import pymongo
from info import DATABASE_URI, DATABASE_NAME

# MongoDB connection setup
myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
creds_collection = mydb['gdrive_creds']

# Thread lock for safe concurrent access
INSERTION_LOCK = threading.RLock()

def _set(chat_id, credential_string):
    with INSERTION_LOCK:
        credential_string = pickle.dumps(credential_string)
        creds_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"credential_string": credential_string}},
            upsert=True
        )

def search(chat_id):
    with INSERTION_LOCK:
        saved_cred = creds_collection.find_one({"chat_id": chat_id})
        creds = None
        if saved_cred:
            creds = pickle.loads(saved_cred['credential_string'])
        return creds

def _clear(chat_id):
    with INSERTION_LOCK:
        creds_collection.delete_one({"chat_id": chat_id})

# Example usage of sync functions
def set_creds(chat_id, credential_string):
    _set(chat_id, credential_string)

def get_creds(chat_id):
    return search(chat_id)

def clear_creds(chat_id):
    _clear(chat_id)
