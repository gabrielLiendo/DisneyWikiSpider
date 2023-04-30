import sys
from neo4j import GraphDatabase

if len(sys.argv) != 2 or not sys.argv[1].isnumeric():
    print('''\nRecuerda pasar como argumento el año de las peliculas como:\n\tpython moviesYear.py 2005\n''')
    exit(1)

year = sys.argv[1]

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

# Dado un año YYYY mostrar las películas estrenadas ese año
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Estrenada_en] -> (:Estreno{year: $year}) "
        "RETURN p"
    )
    result = session.run(query, year=year)
    
    print("Las películas estrenadas en el año", year, "son:")
    for record in result.data():
        print(record['p']['titulo'])
    
    driver.close()
    
