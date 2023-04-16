from pymongo import MongoClient

client = MongoClient("mongodb://fast_food:7335140@localhost:27017/?authMechanism=DEFAULT&authSource=fast_food_db")
db = client["fast_food_db"]
