import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def get_embedding_function(embedding_model: str = 'text-embedding-3-small'):

    embedding_function = OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name=embedding_model)

    return embedding_function
