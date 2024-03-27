import os

import dspy
import openai
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def init_dspy(
    database_name: str = "chroma_db",
    language_model_class=dspy.OpenAI,
    max_tokens: int = 500,
    model: str = "gpt-3.5-turbo-instruct",
):
    language_model = language_model_class(
        max_tokens=max_tokens,
        model=model
    )

    class Text(BaseModel):
        text: str
        long_text: str

    def retrieve(query: str, k: int, **kwargs):

        # TODO: Implement a proper retrieval mechanism
        # Here I return text with some information but this should be retrieved from DB.
        # This is to test that RAG system can separate what is "good" and "relevant" from what is not.

        # TODO: @Anna pls replace by proper retrieval mechanism
        opts = [
            "Suzuki couplings are typically performed in the presence of a palladium catalyst --typically Pd(OH)2--, a base, and a solvent like 1,4-dioxane. The reaction is typically carried out at a temperature of 83.91 degrees Celsius.",
            "The Heck reaction is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
            "A strange suzuki coupling was performed in the presence of a palladium catalyst, a base, and a solvent which can be toluene or THF. The reaction is typically carried out at a temperature of 6.230 degrees Celsius.",
            "102.5 degrees Celsius is the optimal temperature for a suzuki coupling reaction, specially with water as solvent.",
            "THF is typically used for suzuki compulings but we found that using this has very low yields.",
            "The Sonogashira reaction is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
            "The Buchwald-Hartwig amination is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
        ]
        return [Text(text=opts[i], long_text=opts[i]) for i in range(k)]
    
    dspy.settings.configure(lm=language_model, rm=retrieve)


