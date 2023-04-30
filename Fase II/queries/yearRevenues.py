from neo4j import GraphDatabase

uri = "neo4j+s://bb2d6636.databases.neo4j.io"
auth = ("neo4j", "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI")
driver = GraphDatabase.driver(uri, auth=auth)

# Mostrar el año con mayores fondos recaudados.
with driver.session() as session:
    query = (
        "MATCH (p:Pelicula) - [:Estrenada_en] -> (e:Estreno) "
        "RETURN e.year AS year, SUM(p.taquilla) AS taquilla_acumulada " 
        "ORDER BY taquilla_acumulada DESC LIMIT 1" 
    )
    result = session.run(query)
    for record in result.data():
        print("El año con mayores fondos recaudados fue", record['year'], "con", f"{ record['taquilla_acumulada']:,}", "dolares")
    
    driver.close()