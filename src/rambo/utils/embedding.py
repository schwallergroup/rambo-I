from chromadb.api.types import Documents
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import EmbeddingFunction


def get_embedding_function() -> EmbeddingFunction[Documents] | None:
    """Get the default embedding function for documents.

    Returns:
        An instance of EmbeddingFunction[Documents] or None if not found.
    """
    return embedding_functions.DefaultEmbeddingFunction()
