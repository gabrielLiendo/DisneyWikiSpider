import sys
import pymongo

if len(sys.argv) < 2:
    print('''\nRecuerda pasar como argumentos los generos de la siguiente manera:\n\tpython moviesGenres.py "Comedia" "Aventura"\n''')
    exit(1)

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

genres = sys.argv[1:]
for i in range(len(genres)):
    tmp = ""
    for token in genres[i].split(" "):
        tmp += token.capitalize() + " "
    genres[i] = tmp[:-1]

# Películas que sean de uno o más géneros dados
q = collection_movies.find({
    'genres': {"$all": genres}
})

print("Las películas con géneros", " ".join(genres), " son:")
for movie in q:
    print(movie['title'])