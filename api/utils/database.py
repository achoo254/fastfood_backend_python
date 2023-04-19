from pymongo import MongoClient
import settings

client = MongoClient("mongodb://fast_food:7335140@localhost:" + settings.PORT_MONGO + "/?authMechanism=DEFAULT&authSource=fast_food_db")
db = client["fast_food_db"]
