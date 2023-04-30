import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

year =  sys.argv[1]

#Dado un año YYYY mostrar las películas estrenadas ese año
q = collection_movies.find({
    'year': year
})

print("Las películas estrenadas en el año", year, "son:")
for movie in q:
    print(movie['title'])