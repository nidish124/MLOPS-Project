import sys
import os
import json
from NetworkSecurity.Logging.logger import logging
from NetworkSecurity.Execption import execption
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_DB_connect = os.getenv("MONGO_DB_URL")
print("MongoDB Connection URL:", MONGO_DB_connect)

import certifi
CA = certifi.where()

from pymongo import MongoClient
import pandas as pd
import numpy as np

class NetworkDataExtractor:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise execption.Custom_execption(e, sys)
    
    def csv_to_json(self, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            df = df.reset_index(drop=True)
            records = json.loads(df.to_json(orient='records'))
            return records
        except Exception as e:
            logging.error("Error occurred while converting CSV to JSON: %s", e)
            raise execption.Custom_execption(e, sys)
    
    def json_to_mongodb(self, json_data):
        try:
            client = MongoClient(MONGO_DB_connect, tlsCAFile=CA)
            db = client['NetworkSecurity']
            collection = db['Network_Data']
            collection.insert_many(json_data)
            logging.info("Data inserted successfully into MongoDB")
            return len(json_data)

        except Exception as e:
            logging.info("Error occurred while inserting data into MongoDB: %s", e)
            raise execption.Custom_execption(e, sys)
        

if __name__ == "__main__":
    ext = NetworkDataExtractor()
    csv_file_path = 'Network_Data\phisingData.csv'
    try:
        json_data = ext.csv_to_json(csv_file_path)
        inserted_count = ext.json_to_mongodb(json_data)
        print(f"Inserted {inserted_count} records into MongoDB.")
    except execption.Custom_execption as e:
        raise execption.Custom_execption(e, sys)