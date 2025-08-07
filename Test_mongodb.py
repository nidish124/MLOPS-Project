from pymongo.mongo_client import MongoClient
import certifi

uri = "mongodb+srv://nidish124:Fzdu1xh1KVRxrwcD@cluster0.eljwo6j.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)