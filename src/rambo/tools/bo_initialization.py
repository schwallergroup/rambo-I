"""Main functionality for RAG model."""

import dspy
from pydantic import BaseModel, Field
from typing import List
from dspy.functional import TypedPredictor
from .retrieve import ReActRetrieve


class BojanaOutput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """
    temperature: float = Field(description="Temperature to use.")
    solvent: str = Field(description="Solvent to use.")
    catalyst: str = Field(description="Catalyst to use.")
    # TODO add more fields @Bojana?


class BOSignature(dspy.Signature):
    """Suggest initial conditions to start BO."""

    context = dspy.InputField(desc="Relevant conditions used in other reactions found in the literature.")
    query = dspy.InputField(desc="User query, specifies problem and constraints.")
    n = dspy.InputField(desc="Give n conditions to start BO.")
    conditions: List[BojanaOutput] = dspy.OutputField(desc="Initial conditions to start BO.")


class BOInitializer(dspy.Module):
    """Initialize the BO module."""
    def __init__(self, n: int = 5):
        super().__init__()

        self.n = str(n)
        self.retrieve = ReActRetrieve(n)
        self.predict = TypedPredictor(BOSignature)

    def forward(self, query):
        """Forward pass of the BO module."""
        context = self.retrieve(query=query)
        pred = self.predict(context=context, query=query, n=self.n)
        return pred

