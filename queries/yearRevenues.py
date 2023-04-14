import sys
import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_movies = db['movies']

#Mostrar el año con mayores fondos recaudados.
q = collection_movies.aggregate([
    {   
        "$group": {
            "_id": "$year" ,
            "acummulated_revenue": { "$sum": "$gross_revenue" }
        }
    },
    { "$sort": {"acummulated_revenue": -1} },
])

for record in q:
    #print(record)
    print("El año con mayores fondos recaudados fue", record['_id'], "con", record['acummulated_revenue'], "dolares")