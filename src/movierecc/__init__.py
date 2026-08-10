import chromadb
from pprint import pprint
import chromadb.utils.embedding_functions as embedding_functions
from dotenv import load_dotenv
import uuid 

load_dotenv()

google_ef = embedding_functions.GoogleGenaiEmbeddingFunction(
    model_name="gemini-embedding-001",
    task_type="SEMANTIC_SIMILARITY"
)

chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection(name="movies", embedding_function=google_ef)
# collection.add(
#     ids = ["movie1", "movie2"],
#     documents=[
#         "The Dark Knight",
#         "Superman"
#     ]
# )
results = collection.query(
    query_texts=["batman"],
    n_results=3

)

pprint(results)