import json
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']
collection_sagas = db['sagas']

with open('data/movies_saga.json') as f:
    data_movies = json.load(f)
    
with open('data/sagas.json') as f:
    data_sagas= json.load(f)
    
collection_movies.insert_many(data_movies)
collection_sagas.insert_many(data_sagas)

client.close()