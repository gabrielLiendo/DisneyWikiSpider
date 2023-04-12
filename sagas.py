import json

with open('data/movies.json', 'r', encoding='utf-8') as movies_json:
    movies = json.load(movies_json)
    if movies is None:
        exit(1)
    print("loaded")