import sys
import pymongo 

if len(sys.argv) != 2 or not sys.argv[1].isnumeric():
    print('''\nRecuerda pasar como argumento el año de las peliculas como:\n\tpython moviesYear.py 2005\n''')
    exit(1)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

year = sys.argv[1]

# Dado un año YYYY mostrar las películas estrenadas ese año
q = collection_movies.find({
    'year': year
})

print("Las películas estrenadas en el año", year, "son:")
for movie in q:
    print(movie['title'])