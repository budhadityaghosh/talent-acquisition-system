import chromadb
from chromadb.utils import embedding_functions
import os

CHROMA_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "dashboard", "chroma_db")
)

def get_chroma():

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name="jobs_collection",
        embedding_function=embedding_function
    )

    return collection