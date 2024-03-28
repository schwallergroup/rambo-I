"""Main functionality for RAG model."""

from typing import List, Optional

import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field
from typing import Literal

from rambo.tools.retrieval import ReActRetrieve
from .design_space import get_design_space

design_space = get_design_space()
# Defining the choices as Literal types
# TODO
# choices_reactant_1 is design_space['reactant_1'] cast to a string where each list tiem is separated by a comma
choices_reactant_1 = design_space['reactant_1'][0]
choices_reactant_2 = design_space['reactant_2'][0]
choices_catalyst = design_space['catalyst'][0]
choices_ligand = design_space['ligand'][0]
choices_reagent = design_space['reagent'][0]
choices_solvent = design_space['solvent'][0]

print(choices_reactant_1)
print(choices_reactant_2)
print(choices_catalyst)
print(choices_ligand)
print(choices_reagent)
print(choices_solvent)


class BOInput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """
    reactant_1: List[str] = Field(description=f"Reactant 1 to use. The choices are {choices_reactant_1}")
    reactant_2: List[str] = Field(description=f"Reactant 2 to use. The choices are {choices_reactant_2}")
    catalyst: List[str] = Field(description=f"Catalyst to use. The choices are {choices_catalyst}")
    ligand: List[str] = Field(description=f"Ligand to use. The choices are {choices_ligand}")
    reagent: List[str] = Field(description=f"Reagent to use. The choices are {choices_reagent}")
    solvent: List[str] = Field(description=f"Solvent to use. The choices are {choices_solvent}")

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
