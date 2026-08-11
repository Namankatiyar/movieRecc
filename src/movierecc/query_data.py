from dotenv import load_dotenv
import os
import vecs
from langchain_openai import AzureOpenAIEmbeddings

load_dotenv()
db_pass = os.getenv("DB_PASSWORD")

DB_CONNECTION = f"postgresql://postgres.yynkzwxttjasrwcjptmg:{db_pass}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"



embedings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large" 
)


with vecs.create_client(DB_CONNECTION) as vx:
     movies_vectordata = vx.get_or_create_collection(name="movies_vectordata", dimension=3072)

     query_vector = embedings.embed_query("Stuck in a dream")
     results = movies_vectordata.query(data=query_vector, limit=5, include_metadata=True)
     for item in results:
        print(item[1]["series_title"])