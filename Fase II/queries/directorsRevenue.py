from neo4j import GraphDatabase

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

# Ordenar de manera ascendente los directores y la cantidad de dinero recaudado según sus películas dirigidas
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Dirigida_por] -> (d:Director) "
        "RETURN d.nombre AS nombre, SUM(p.taquilla) AS taquilla_acumulada " 
        "ORDER BY d.nombre"
    )
    result = session.run(query)
    print("La cantidad de dinero recaudada por cada director es: ")
    for record in result.data():
         print(record['nombre'] + ": " + str( f"{ record['taquilla_acumulada'] :,}" ) +"$")
    
    driver.close()