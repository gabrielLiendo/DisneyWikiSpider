import sys
from neo4j import GraphDatabase

if len(sys.argv) != 2 or not sys.argv[1].isnumeric():
    print('''\nRecuerda pasar como argumento el año de las peliculas como:\n\tpython yearDuration.py 2005\n''')
    exit(1)

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

year = sys.argv[1]

# Dado un año mostrar la película con mayor duración de ese año.
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Estrenada_en] -> (e:Estreno) "
        "WHERE e.year = $year AND p.duracion > 0 "
        "RETURN p "
        "ORDER BY p.duracion DESC LIMIT 1 "
    )
    result = session.run(query, year=year)
    
    for record in result.data():
        print('La película con mayor duración del año', year, 'es', record['p']['titulo'], 'con', record['p']['duracion'], 'minutos')
    
    driver.close()