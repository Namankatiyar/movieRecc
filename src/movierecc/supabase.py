from dotenv import load_dotenv
import os
import vecs
from langchain_openai import AzureOpenAIEmbeddings
import sqlite3
import uuid
import time

load_dotenv()
db_pass = os.getenv("DB_PASSWORD")

DB_CONNECTION = f"postgresql://postgres.yynkzwxttjasrwcjptmg:{db_pass}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"



embedings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large" 
)


with vecs.create_client(DB_CONNECTION) as vx:
    with sqlite3.connect("/home/naman/Documents/movieRecc/imdb_top_1000.db") as con:

        movieIds = []
        movieData = []
        movieMetadata = []

        cursor = con.cursor()
        for i in range(0,1001, 100):
            cursor.execute("SELECT * from imdb_top_1000 ORDER BY ROWID ASC LIMIT 100 OFFSET ?",(i,))
            data = cursor.fetchall() 
            for item in data:
                poster_link, series_title, r_year, genre, imdb, summary, meta_score, director, star1, star2, star3, star4  = item

                movieIds.append(str(uuid.uuid4()))

                movieData.append(f"{series_title} ({r_year}) is a {genre} film directed by {director}, starring {star1}, {star2}, {star3}, and {star4}. {summary}")

                movieMetadata.append(dict(poster_link=poster_link, series_title=series_title, r_year=r_year, genre=genre, imdb=imdb, meta_score=meta_score, director=director, star1=star1, star2=star2, star3=star3, star4=star4))

            embedding_listdata = []
            vector_list = embedings.embed_documents(movieData)
            
            #creating upsert record tuples
            moviedata_list = []
            for i in range(0, len(movieIds)):
                moviedata_list.append((movieIds[i], vector_list[i], movieMetadata[i]))

            movies_vectordata = vx.get_or_create_collection(name="movies_vectordata", dimension=3072)
            movies_vectordata.upsert(
                moviedata_list
            )
            
            print("sleeping...")
            time.sleep(30)

            print("proceeding to next")

    con.close()