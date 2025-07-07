import pymongo
import sys
from pathlib import Path
from db.db_client import DatabaseClient
import json

db_client = DatabaseClient(db_name="JobReco")
mongo_client = db_client.client
database = mongo_client["JobReco"]
database.drop_collection("Jobs")
collection = database["Jobs"]

json_path = Path(__file__).parent.joinpath("data/naukri_output_merged.json")
with open(json_path, "r") as file:
    data = json.load(file)

if isinstance(data, list):
    collection.insert_many(data)
            # If the json file contains a single document
else:
    collection.insert_one(data)

count = len(collection.find({}).to_list())
logger.info(f"{count} no. of data entered.")