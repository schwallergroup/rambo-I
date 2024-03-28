from pydantic import BaseModel
from typing import List

class Text(BaseModel):
    """
    Represents a text object with two properties: text and long_text.
    """
    text: str
    long_text: str

class DummyRetrievalModel:
    """
    Represents a dummy retrieval model.
    """

    def __init__(self):
        """
        Initializes a new instance of the DummyRetrievalModel class.
        """
        self.opts = [
            "Suzuki couplings are typically performed in the presence of a palladium catalyst --typically Pd(OH)2--, a base, and a solvent like 1,4-dioxane. The reaction is typically carried out at a temperature of 83.91 degrees Celsius.",
            "The Heck reaction is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
            "A strange suzuki coupling was performed in the presence of a palladium catalyst, a base, and a solvent which can be toluene or THF. The reaction is typically carried out at a temperature of 6.230 degrees Celsius.",
            "102.5 degrees Celsius is the optimal temperature for a suzuki coupling reaction, specially with water as solvent.",
            "THF is typically used for suzuki compulings but we found that using this has very low yields.",
            "The Sonogashira reaction is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
            "The Buchwald-Hartwig amination is typically performed in the presence of a palladium catalyst, a base, and a solvent. The reaction is typically carried out at a temperature of 80-100 degrees Celsius.",
        ]

    def retrieve(self, query: str, k: int, **kwargs) -> List[Text]:
        """
        Retrieves a list of Text objects based on the given query and the number of results to retrieve.

        Args:
            query (str): The query string.
            k (int): The number of results to retrieve.
            **kwargs: Additional keyword arguments.

        Returns:
            List[Text]: A list of Text objects.
        """
        return [Text(text=self.opts[i], long_text=self.opts[i]) for i in range(min(k, len(self.opts)))]

def get_dummy_retriever() -> DummyRetrievalModel:
    """
    Returns an instance of the DummyRetrievalModel class.

    Returns:
        DummyRetrievalModel: An instance of the DummyRetrievalModel class.
    """
    return DummyRetrievalModel()