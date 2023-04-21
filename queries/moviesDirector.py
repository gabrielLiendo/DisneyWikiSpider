import sys
import pymongo 

if len(sys.argv) != 2:
    print('''\nRecuerda pasar como argumento el nombre del director de la siguiente manera:\n\tpython moviesDirector.py "John Lasseter"\n''')
    exit(1)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

director = ""

for name in sys.argv[1].split(" "):
    director += name.capitalize() + " "

director = director[:-1]

# Cantidad de películas dado un director.
q = collection_movies.count_documents({
    'director': director
})

print("El director", director, "tiene", q, "películas")