import sys
from neo4j import GraphDatabase

if len(sys.argv) != 2:
    print('''\nRecuerda pasar como argumento el nombre del director de la siguiente manera:\n\tpython moviesDirector.py "John Lasseter"\n''')
    exit(1)
    
director = ""

for name in sys.argv[1].split(" "):
    director += name.capitalize() + " "

director = director[:-1]

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Dirigida_por] -> (d:Director{nombre: $director}) "
        "RETURN COUNT(p)"
    )
    result = session.run(query, director=director)
    
    print("El director", director, "tiene", result.single()[0], "películas")
    
    driver.close()