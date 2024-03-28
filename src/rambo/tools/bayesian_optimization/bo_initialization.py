"""Main functionality for RAG model."""

from typing import List, Optional

import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field

from rambo.tools.retrieval import ReActRetrieve


class BOInput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """

    reactant_1: str = Field(description="Reactant 1 to use.")
    reactant_2: str = Field(description="Reactant 2 to use.")
    catalyst: str = Field(description="Catalyst to use.")
    ligand: str = Field(description="Ligand to use.")
    reagent: str = Field(description="Reagent to use.")
    solvent: str = Field(description="Solvent to use.")

    # input_param_values = DesignSpace
    # TODO add more fields @Bojana?


class BOSignature(dspy.Signature):
    """Suggest initial conditions to start BO."""

    context = dspy.InputField(
        desc="Relevant conditions used in other reactions found in the literature."
    )
    query = dspy.InputField(
        desc="User query, specifies problem and constraints."
    )
    n = dspy.InputField(desc="Give n conditions to start BO.")
    conditions: List[BOInput] = dspy.OutputField(
        desc="Initial conditions to start BO."
    )


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
