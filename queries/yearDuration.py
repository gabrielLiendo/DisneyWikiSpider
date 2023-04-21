import sys
import pymongo

if len(sys.argv) != 2 or not sys.argv[1].isnumeric():
    print('''\nRecuerda pasar como argumento el año de las peliculas como:\n\tpython yearDuration.py 2005\n''')
    exit(1)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

year = sys.argv[1]

# Dado un año mostrar la película con mayor duración de ese año.
q = collection_movies.aggregate([
    {'$match': {'year': year}},
    {'$sort': {'duration': -1}},
    {'$limit': 1}
])

for movie in q:
    print('La película con mayor duración del año', year, 'es', movie['title'], 'con', movie['duration'], 'minutos')