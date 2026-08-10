import chromadb
from pprint import pprint
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import uuid 
import sqlite3
from google import genai
import time
from google.genai import types


load_dotenv()
client = genai.Client()


google_ef = embedding_functions.GoogleGenaiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="RETRIEVAL_DOCUMENT"
)

chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection(name="movies", embedding_function=google_ef)

movieIds = []
movieData = []
movieMetadata = []

with sqlite3.connect("/home/naman/Documents/movieRecc/imdb_top_1000.db") as con:

    cursor = con.cursor()
    for i in range(0,1001, 100):
        cursor.execute("SELECT * from imdb_top_1000 ORDER BY ROWID ASC LIMIT 100 OFFSET ?",(i,))
        data = cursor.fetchall() 
        for item in data:
            poster_link, series_title, r_year, genre, imdb, summary, meta_score, director, star1, star2, star3, star4  = item

            movieIds.append(str(uuid.uuid4()))

            movieData.append(f"{series_title} ({r_year}) is a {genre} film directed by {director}, starring {star1}, {star2}, {star3}, and {star4}. {summary}")

            movieMetadata.append(dict(poster_link=poster_link, series_title=series_title, r_year=r_year, genre=genre, imdb=imdb, meta_score=meta_score, director=director, star1=star1, star2=star2, star3=star3, star4=star4))

        embedding_list = []

        for i in range(0,len(movieData)):
            embedding_object = client.models.batchEmbedContent(
                model="gemini-embedding-001",
                contents=movieData[i],
                config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
            )
            embedding_list.append(embedding_object.embeddings[0].values)
            
            print(i)

        print("batch completed")

        
        collection.add(ids=movieIds, documents=movieData, metadatas=movieMetadata, embeddings=embedding_list)
        movieIds = []
        movieData = []
        movieMetadata = []

con.close()

# results = collection.query(query_texts=["stuck in a dream"], n_results=10)

# pprint(results)
