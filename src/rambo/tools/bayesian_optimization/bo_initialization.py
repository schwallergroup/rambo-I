"""Main functionality for RAG model."""

from typing import Annotated, List, Literal, Optional

import dspy
from dspy.functional import TypedPredictor
from pydantic import BaseModel, Field

from rambo.tools.retrieval import ReActRetrieve

from .design_space import get_design_space

design_space = get_design_space()
choices_reactant_1 = tuple(design_space["reactant_1"])
choices_reactant_2 = tuple(design_space["reactant_2"])
choices_catalyst = tuple(design_space["catalyst"])
# Limit to 5 choices for ease
choices_ligand = tuple(design_space["ligand"][:5])
choices_reagent = tuple(design_space["reagent"][:5])
choices_solvent = tuple(design_space["solvent"][:5])


class BOInput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """
    reactant_1: Literal[choices_reactant_1] = Field(desc=f"Reactant 1 to use.")
    reactant_2: Literal[choices_reactant_2] = Field(desc=f"Reactant 2 to use.")
    catalyst: Literal[choices_catalyst] = Field(desc=f"Catalyst to use.")
    ligand: Literal[choices_ligand] = Field(desc=f"Ligand to use.")
    reagent: Literal[choices_reagent] = Field(desc=f"Reagent to use.")
    solvent: Literal[choices_solvent] = Field(desc=f"Solvent to use.")
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
        print(context)
        pred = self.predict(context=context, query=query, n=self.n)
        return pred
