import sys
import pymongo 

if len(sys.argv) != 3:
    print('''\nRecuerda pasar como argumento la calificacion minima y maxima de la siguiente manera:\n\tpython moviesRanking.py 3.0 5.0\n''')
    exit(1)

try:
    min = float(sys.argv[1])
    max = float(sys.argv[2])
except:
    print('''\nRecuerda pasar como argumento la calificacion minima y maxima de la siguiente manera:\n\tpython moviesRanking.py 3.0 5.0\n''')
    exit(1)

if min > max:
    tmp = min
    min = max
    max = tmp

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

# Dado un rango (N, M) mostrar las películas que se encuentren en ese ranking según IMDB.
q = collection_movies.find({
    'imdb_rating': { "$gt" :  float(min), "$lt" : float(max)}
})

print("Las películas con un rating en IMDB entre", min, "y", max, "son:")
for movie in q:
    print(movie['title'], movie['imdb_rating'])