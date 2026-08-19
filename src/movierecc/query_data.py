from dotenv import load_dotenv
import os
import vecs
from langchain_openai import AzureOpenAIEmbeddings
from supabase import create_client, Client
from pprint import pprint
import json 

load_dotenv()
db_pass = os.getenv("DB_PASSWORD")
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

response = (supabase.schema("public")
            .table("movie_metadata")
            .select("id")
            .eq("series_title", "Inception")
            .execute())

print((response.data))

id = response.data[0].get("id")

responseVector = (supabase.schema("vecs")
                  .table("movies_vectordata")
                  .select("vec")
                  .eq("id", id)
                  .execute())

query_vector = json.loads(responseVector.data[0].get("vec"))

DB_CONNECTION = f"postgresql://postgres.yynkzwxttjasrwcjptmg:{db_pass}@aws-0-ap-south-1.pooler.supabase.com:5432/postgres"

embedings = AzureOpenAIEmbeddings(
    model="text-embedding-3-large" 
)

with vecs.create_client(DB_CONNECTION) as vx:
    movies_vectordata = vx.get_or_create_collection(name="movies_vectordata", dimension=3072)

    results = movies_vectordata.query(data=query_vector, limit=20, include_metadata=True)
    for item in results:
        print(item[1]["series_title"])

