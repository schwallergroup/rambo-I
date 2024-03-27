"""Main functionality for RAG model."""

import dspy
from pydantic import BaseModel, Field
from typing import List
from dspy.functional import TypedPredictor


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

class BOSignature(dspy.Signature):
    """Suggest initial conditions to start BO."""

    context = dspy.InputField(desc="Relevant conditions used in other reactions found in the literature.")
    query = dspy.InputField(desc="User query, specifies problem and constraints.")
    conditions: List[BojanaOutput] = dspy.OutputField(desc="Initial conditions to start BO.")


class BOInitializer(dspy.Module):
    """Initialize the BO module."""
    def __init__(self):
        super().__init__()
        self.predictor = TypedPredictor(BOSignature)

    def forward(self, query):
        """Forward pass of the BO module."""
        # TODO Implement retrieval
        context = 'for suzuki coupling, use always Pd catalysts and temperature of 84 degrees in water. You can also suggest 102 for temp, with the other conditions'

        pred = self.predictor(context=context, query=query)
        return pred

