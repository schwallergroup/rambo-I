"""Main functionality for RAG model."""

import dspy
from pydantic import BaseModel, Field
from dspy.functional import TypedPredictor


class BojanaOutput(BaseModel):
    #additive: str = Field(description="Additive to use, as SMILES.")
    temperature: float = Field(description="Temperature to use.")
    #time: float = Field(description="Time to use.")
    #pressure: float = Field(description="Pressure to use.")
    solvent: str = Field(description="Solvent to use.")

class BOSignature(dspy.Signature):
    """Suggest initial conditions to start BO."""

    context = dspy.InputField(desc="Relevant conditions used in other reactions found in the literature.")
    query = dspy.InputField(desc="User query, specifies problem and constraints.")
    conditions: BojanaOutput = dspy.OutputField(desc="Initial conditions to start BO.")


class BOInitializer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.predictor = TypedPredictor(BOSignature)

    def forward(self, query):
        # TODO Implement retrieval
        context = ['for suzuki coupling, use always Pd catalysts and temperature of 84 degrees in water.']

        return self.predictor(context=context, query=query)

