from neo4j import GraphDatabase

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

# De existir una saga. Mostrar las películas asociadas.
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Pertenece_a_la_saga] -> (s:Saga) "
        "RETURN s.nombre AS nombre, COLLECT(DISTINCT p.titulo) AS peliculas " 
    )
    result = session.run(query)
    print("Las sagas encontradas y sus películas asociadas son:")
    for record in result.data():
        print(record['nombre'], ":", record['peliculas'])
    
    driver.close()