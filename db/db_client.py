# db_client.py
import json
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure
from db.jobs_schema import JobDocument
from log.logger import logger
class DatabaseClient:
    """
    A generic client for interacting with a MongoDB database.
    """

    def __init__(self, host='localhost', port=27017, db_name='JobReco'):
        """
        Initializes the connection to the MongoDB server and selects a database.

        Args:
            host (str): The database server host.
            port (int): The database server port.
            db_name (str): The name of the database to connect to.
        """
        try:
            connection_string = f'mongodb://{host}:{port}/'
            self.client = MongoClient(connection_string)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.db = self.client[db_name]
            logger.info(f"✅ Successfully connected to MongoDB database: '{db_name}'")
        except ConnectionFailure as e:
            logger.error(f"❌ Could not connect to MongoDB: {e}")
            self.client = None
            self.db = None

    def insert_from_json(self, collection_name, file_path):
        """
        Inserts data from a JSON file into a specified collection.

        Args:
            collection_name (str): The name of the collection.
            file_path (str): The path to the JSON file.

        Returns:
            bool: True if insertion was successful, False otherwise.
        """
        if self.db is None:
            print("❌ Cannot insert data, no database connection.")
            return False
        
        collection = self.db[collection_name]
        print(f"\n Inserting data from '{file_path}' into collection '{collection_name}'...")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # If the json file contains a list of documents
            if isinstance(data, list):
                collection.insert_many(data)
            # If the json file contains a single document
            else:
                collection.insert_one(data)
            
            print("✅ Data inserted successfully.")
            return True
        except FileNotFoundError:
            print(f"❌ Error: The file '{file_path}' was not found.")
            return False
        except Exception as e:
            print(f"❌ An error occurred during insertion: {e}")
            return False

    def run_query(self, collection_name, query={}, DocumentType=JobDocument):
        """
        Runs a query on a specified collection.

        Args:
            collection_name (str): The name of the collection to query.
            query (dict): The MongoDB query filter. An empty dict {} will find all documents.

        Returns:
            list: A list of documents matching the query, or an empty list if an error occurs.
        """
        if self.db is None:
            print("❌ Cannot run query, no database connection.")
            return []
        collection = self.db.get_collection(collection_name)

        print("collection name :", collection, type(collection))
        print(f"\n🔍 Running query on '{collection_name}': {query}")
        try:
            query_results = collection.find(query).to_list()
            def process_results(result):
                if "_id" in result:
                    result["_id"] = str(result["_id"])
                return result
            processed_result = list(map(process_results, query_results))
            print("✅ Query executed successfully.")
            return processed_result
        except Exception as e:
            print(f"❌ An error occurred while running the query: {e}")
            return []

    def close_connection(self):
        """
        Closes the connection to the MongoDB server.
        """
        if self.client:
            self.client.close()
            print("\n🔌 Connection to MongoDB closed.")
            
            
if __name__ == "__main__":
    db_client = DatabaseClient(db_name="JobReco")
    results = db_client.run_query("Jobs", {"title": {"$regex": "Developer"}})
    print(results)
    print(len(results))

    db_client.close_connection()