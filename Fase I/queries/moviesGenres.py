import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

genres =  sys.argv[1:]

#Películas que sean de uno o más géneros dados
q = collection_movies.find({
    'genres': {"$all": genres}
})

print("Las películas con géneros", genres, "son:")
for movie in q:
    print(movie['title'])