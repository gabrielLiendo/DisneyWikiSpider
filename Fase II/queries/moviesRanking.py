import sys
from neo4j import GraphDatabase

if len(sys.argv) != 3:
    print('''\nRecuerda pasar como argumento la calificacion minima y maxima de la siguiente manera:\n\tpython moviesRanking.py 3.0 5.0\n''')
    exit(1)

try:
    min = float(sys.argv[1])
    max = float(sys.argv[2])
except:
    print('''\nRecuerda pasar como argumento la calificacion minima y maxima de la siguiente manera:\n\tpython moviesRanking.py 3.0 5.0\n''')
    exit(1)

if min > max:
    tmp = min
    min = max
    max = tmp

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

# Dado un rango (N, M) mostrar las películas que se encuentren en ese ranking según IMDB.
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) "
        "WHERE $min < p.rating_imdb < $max "
        "RETURN p "
    )
    result = session.run(query, min=min, max=max)
    
    print("Las películas con un rating en IMDB entre", min, "y", max, "son:")
    for record in result.data():
        print(record['p']['titulo'], record['p']['rating_imdb'])
    
    driver.close()