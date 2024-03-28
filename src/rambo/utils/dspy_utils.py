import os

import dspy
import openai
from dotenv import load_dotenv
from dspy.retrieve.chromadb_rm import ChromadbRM
from pydantic import BaseModel

from rambo.tools.retrieval import get_dummy_retriever, get_embedding_function

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")


def init_dspy(
    database_name: str = "text-embedding-3-small_text_description",
    language_model_class=dspy.OpenAI,
    max_tokens: int = 500,
    model: str = "gpt-4-0613",
    retrieval_type: str = "embedding",
):
    language_model = language_model_class(max_tokens=max_tokens, model=model)

    if retrieval_type == "embedding":
        embedding_function = get_embedding_function()
        retrieval_model = ChromadbRM(
            collection_name=database_name,
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_function,
        )

    elif retrieval_type == "test":
        retrieval_model = get_dummy_retriever().retrieve

    elif retrieval_type == "agent":
        # TODO @ Andres: Implement agent retrieval, maybe you need to edit the return statement?
        # rn we pass a model as the rm param in the dspy settings
        pass

    else:
        raise ValueError(
            f"Unknown retrieval type: {retrieval_type}, choose from 'embedding', 'test', 'agent'"
        )

    dspy.settings.configure(lm=language_model, rm=retrieval_model)
