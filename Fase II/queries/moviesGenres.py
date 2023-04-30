import sys
from neo4j import GraphDatabase

if len(sys.argv) < 2:
    print('''\nRecuerda pasar como argumentos los generos de la siguiente manera:\n\tpython moviesGenres.py "Comedia" "Aventura"\n''')
    exit(1)
    
genres = sys.argv[1:]
for i in range(len(genres)):
    tmp = ""
    for token in genres[i].split(" "):
        tmp += token.capitalize() + " "
    genres[i] = tmp[:-1]
    
uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

with driver.session() as session:
    query = "MATCH "  + ', '.join("(p:Pelicula) - [:Es_del_genero] -> (:Genero{nombre:'" + s +"'})" for s in genres) + " RETURN p"

    result = session.run(query)
    
    print("Las películas con géneros", " ".join(genres), "son:")
    for record in result.data():
        print(record['p']['titulo'])
    
    driver.close()