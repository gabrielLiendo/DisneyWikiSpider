from pymongo import MongoClient
from neo4j import GraphDatabase
from bson.json_util import dumps
import json

class ETL:
  def __init__(self, mongo_uri, neo4j_uri, user, password):
    self.client = MongoClient(mongo_uri)
    self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(user, password))
    self.movies = []

  def close(self):
    self.neo4j_driver.close()
    
  def extract_movies(self):
    db = self.client['disney_db']
    cursor = db['movies'].find()
    self.movies = json.loads(dumps(cursor))

  def load_movies(self):
    with self.neo4j_driver.session() as session:

      query = (
        "UNWIND $movies AS movie "
        #Insert Movie Node
        "CREATE (p:Pelicula {titulo_original: movie.original_title, duracion: movie.duration, taquilla: movie.gross_revenue, rating_imdb:movie.imdb_rating, clasificacion: movie.parental_guide, titulo: movie.title}) "
        #Insert Directors Nodes
        "WITH p, movie, movie.director as directors "
        "FOREACH (director IN directors  | "
          "MERGE (d:Director {nombre: director}) "
          "CREATE (p) - [:Dirigida_por] -> (d) "
        ") "
        "WITH movie, p "
        #Insert Year Node
        "CALL apoc.do.when( movie.year IS NOT NULL, 'MERGE (a:Estreno {year: year}) CREATE (p) - [:Estrenada_en] -> (a) RETURN p', 'RETURN p', {year:movie.year, p:p} ) YIELD value "
        #Insert Genres Nodes
        "WITH p, movie, movie.genres as generos "
        "FOREACH (genero IN generos | "
          "MERGE (g:Genero {nombre: genero}) "
          "CREATE (p) - [:Es_del_genero] -> (g) "
        ") "
        #Insert Studio Nodes
        "WITH p, movie, movie.studio as estudios "
        "FOREACH (estudio IN estudios| "
          "MERGE (e:Estudio {nombre: estudio}) "
          "CREATE (p) - [:Producida_por] -> (e) "
        ") "
        #Insert Cast Nodes
        "WITH p, movie, movie.cast as cast "
        "FOREACH (actor IN cast| "
          "MERGE (a:Actor {nombre: actor}) "
          "CREATE (p) <- [:Actua_en] - (a) "
        ") "
        #Insert Awards Nodes
        "WITH p, movie, movie.awards as awards "
        "FOREACH (award IN awards| "
          "MERGE (gd:Galardon {nombre: award.name}) "
          "CREATE (p) - [:Fue_nominada {ganador: award.winner}] -> (gd) "
        ") "
        #Insert Saga Node
        "WITH movie, p "
        "CALL apoc.do.when( movie.saga IS NOT NULL, 'MERGE (s:Saga {nombre: saga}) CREATE (p) - [:Pertenece_a_la_saga] -> (s) RETURN p', 'RETURN p', {saga:movie.saga, p:p} ) YIELD value "
        #Insert Characters Nodes
        "WITH p, movie, movie.characters as characters "
        "FOREACH (personaje IN characters| "
          "MERGE (ps:Personaje {nombre: personaje}) "
          "CREATE (p) <- [:Aparece_en] - (ps) "
        ") "
        "RETURN p "
      )
      
      session.run(query, movies=self.movies)
      
if __name__ == "__main__":
  #Credentials
  mongo_uri = "mongodb+srv://admin:admin@cluster0.jghkftl.mongodb.net/?retryWrites=true&w=majority"
  neo4j_uri = "neo4j+s://bb2d6636.databases.neo4j.io"
  neo4j_user = "neo4j"
  neo4j_password = "TO4OFgnWyrB1K4O0bbF3jzGjNbqVeLvXW2dAPrJLuXI"
  
  etl = ETL(mongo_uri, neo4j_uri, neo4j_user, neo4j_password)
  etl.extract_movies()
  etl.load_movies()
  etl.close()
    