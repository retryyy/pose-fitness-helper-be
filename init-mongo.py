import pymongo
import os
import bcrypt

client = pymongo.MongoClient(
    f'mongodb://{os.environ["MONGO_HOST"]}:{os.environ["MONGO_PORT"]}',
    serverSelectionTimeoutMS=0
)
mongo = client.get_database(os.environ["DB_NAME"])

mongo.users.insert_one({
    'name': 'admin',
    'password': bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
})
