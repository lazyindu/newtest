from pymongo import MongoClient
from bot import DATABASE_URI, LOGGER

def start():
    try:
        client = MongoClient(DATABASE_URI)
        db = client.get_database()
        return db
    except Exception as e:
        LOGGER.error(f'Failed to connect to MongoDB: {e}')
        exit(1)

# Initialize the MongoDB database
db = start()

# Collections
gDriveDB = db['gdrive_credentials']
idsDB = db['gdrive_parent_ids']
