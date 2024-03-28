"""Main functionality for RAG model."""

from typing import List, Optional

import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field
from typing import Literal

from rambo.tools.retrieval import ReActRetrieve
from .design_space import get_design_space

design_space = get_design_space()
choices_reactant_1 = design_space['reactant_1']
choices_reactant_2 = design_space['reactant_2']
choices_catalyst = design_space['catalyst']
choices_ligand = design_space['ligand'][0] # selecting just one element because otherwise the chhoices are too complicated
choices_reagent = design_space['reagent'][0]
choices_solvent = design_space['solvent'][0]

class BOInput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """
    reactant_1: str = Field(desc=f"Reactant 1 to use. The choices are {choices_reactant_1}")
    reactant_2: str = Field(desc=f"Reactant 2 to use. The choices are {choices_reactant_2}")
    catalyst: str = Field(desc=f"Catalyst to use. The choices are {choices_catalyst}")
    ligand: str = Field(desc=f"Ligand to use. The choices are {choices_ligand}")
    reagent: str = Field(desc=f"Reagent to use. The choices are {choices_reagent}")
    solvent: str = Field(desc=f"Solvent to use. The choices are {choices_solvent}")

    # TODO make dynamic from natural language prompt/dataset


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
