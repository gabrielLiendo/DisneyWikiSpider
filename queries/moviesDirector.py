import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

director = ""

for name in sys.argv[1].split(" "):
    director += name.capitalize() + " "

director = director[:-1]

#Cantidad de películas dado un director.
q = collection_movies.count_documents({
    'director': director
})

print("El director", director, "tiene", q, "películas")