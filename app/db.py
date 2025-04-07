from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/hopital?replicaSet=rs0")
client = MongoClient(MONGO_URI)
db = client['hopital']
