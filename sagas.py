import json

movies_json = open('data/movies.json', 'r', encoding='utf-8')
movies = json.load(movies_json)
movies_json.close()

if movies is None:
    exit(1)

sagas = dict()

for movie in movies:
    if "preceded_by" in movie:
        added = False
        for saga_name, saga in sagas.items():
            if movie["preceded_by"] in saga:
                saga.add(movie["title"])
                added = True
                movie["saga"] = saga_name
                break
        if not added:
            sagas["Saga de " + movie["preceded_by"]] = {movie["title"], movie["preceded_by"]}
            movie["saga"] = "Saga de " + movie["preceded_by"]


saga_list = []
for saga_name in sagas.keys():
    saga_list.append({"name":saga_name,  "movies": list(sagas[saga_name]) })

with open("data/sagas.json", 'w') as file:
    json.dump(saga_list, file)

with open("data/movies_saga.json", 'w') as file:
    json.dump(movies, file)

