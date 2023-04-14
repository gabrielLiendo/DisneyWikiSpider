import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

year =  sys.argv[1]

#Dado un año mostrar la película con mayor duración de ese año.
q = collection_movies.aggregate([
    {'$match': {'year': year}},
    {'$sort': {'duration': -1}},
    {'$limit': 1}
])

for movie in q:
    print('La película con mayor duración del año', year, 'es', movie['title'], 'con', movie['duration'], 'minutos')