import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

#Ordenar de manera ascendente los directores y la cantidad de dinero recaudado según sus películas dirigidas
q = collection_movies.aggregate([
    { "$unwind": "$director" },
    {   
        "$group": {
            "_id": "$director" ,
            "acummulated_revenue": { "$sum": "$gross_revenue" }
        }
    },
    { "$sort": {"_id": 1} }
])

for movie in q:
    print(movie)