import json

with open('data/movies.json', 'r', encoding='utf-8') as movies_json:
    movies = json.load(movies_json)
    if movies is None:
        exit(1)

    sagas = dict()

    for movie in movies:
        if "preceded_by" in movie:
            added = False
            for saga in sagas.values():
                if movie["preceded_by"] in saga:
                    saga.add(movie["title"])
                    added = True
                    break
            if not added:
                sagas["Saga de " + movie["preceded_by"]] = {movie["title"], movie["preceded_by"]}

    for saga_name in sagas.keys():
        sagas[saga_name] = list(sagas[saga_name])

    with open("data/sagas.json", 'w') as file:
        json.dump(sagas, file)
