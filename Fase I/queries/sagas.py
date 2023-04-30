import pymongo 

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/test")
db = client['disney_db']
collection_sagas = db['sagas']

# De existir una saga. Mostrar las películas asociadas.
q = collection_sagas.find({})

print("Las sagas encontradas y sus películas asociadas son:")
for saga in q:
    print(saga['name'], ":", saga['movies'])