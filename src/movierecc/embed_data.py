import chromadb
from pprint import pprint
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import uuid 
import sqlite3

load_dotenv()

# google_ef = embedding_functions.GoogleGenaiEmbeddingFunction(
#     model_name="gemini-embedding-001",
#     task_type="RETRIEVAL_DOCUMENT"
# )

with sqlite3.connect("/home/naman/Documents/movieRecc/imdb_top_1000.db") as con:
    cursor = con.cursor()
    cursor.execute("SELECT * from imdb_top_1000 where ROWID <=10")
    data = cursor.fetchall()

    movieIds = []
    movieData = []
    movieMetadata = []

    for item in data:
        poster_link, series_title, r_year, genre, imdb, summary, meta_score, director, star1, star2, star3, star4  = item

        movieIds.append(str(uuid.uuid4()))

        movieData.append(f"{series_title} ({r_year}) is a {genre} film directed by {director}, starring {star1}, {star2}, {star3}, and {star4}. {summary}")

        movieMetadata.append(dict(poster_link=poster_link, series_title=series_title, r_year=r_year, genre=genre, imdb=imdb, meta_score=meta_score, director=director, star1=star1, star2=star2, star3=star3, star4=star4))

con.close()


# chroma_client = chromadb.PersistentClient(path="./db")
# collection = chroma_client.get_or_create_collection(name="movies", embedding_function=google_ef)
# collection.add(
#     ids = ["movie1", "movie2"],
#     documents=[
#         "The Dark Knight",
#         "Superman"
#     ]
# )

