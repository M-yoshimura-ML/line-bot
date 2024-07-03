from dotenv import load_dotenv
from pymongo import MongoClient
import os


load_dotenv()
# Step 1: Connect to MongoDB
credential = os.environ.get('MONGODB_URI')
client = MongoClient(credential)

# Step 2: Access a Database
db = client['shop']  # Replace with your database name

# Step 3: Access a Collection
collection = db['products']  # Replace with your collection name

# Step 4: Retrieve Data
# To find all documents in the collection
documents = collection.find()

# Print retrieved documents
for document in documents:
    print(document)
