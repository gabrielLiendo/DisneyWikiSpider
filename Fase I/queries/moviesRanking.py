import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

min = sys.argv[1]
max = sys.argv[2]

#Dado un rango (N, M) mostrar las películas que se encuentren en ese ranking según IMDB.
q = collection_movies.find({
    'imdb_rating': { "$gt" :  float(min), "$lt" : float(max)}
})

print("Las películas con un rating en IMDB entre", min, "y", max, "son:")
for movie in q:
    print(movie['title'], movie['imdb_rating'])