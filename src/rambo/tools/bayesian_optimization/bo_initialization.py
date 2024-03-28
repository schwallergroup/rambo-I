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
# ChoicesReactant1 = Literal[tuple(design_space['reactant_1'])]
# ChoicesReactant2 = Literal[tuple(design_space['reactant_2'])]
# ChoicesCatalyst = Literal[tuple(design_space['catalyst'])]
# ChoicesLigand = Literal[tuple(design_space['ligand'])]
# ChoicesReagent = Literal[tuple(design_space['reagent'])]
# ChoicesSolvent = Literal[tuple(design_space['solvent'])]


class BOInput(BaseModel):
    """
    Represents the output of the Bojana tool.

    Attributes:
        temperature (float): The temperature to use.
        solvent (str): The solvent to use.
    """
    reactant_1: str = Field(description=f"Reactant 1 to use. The choices are {', '.join(', '.join(design_space['reactant_1']))}")
    reactant_2: str = Field(description=f"Reactant 2 to use. The choices are {', '.join(design_space['reactant_2'])}")
    catalyst: str = Field(description=f"Catalyst to use. The choices are {', '.join(design_space['catalyst'])}")
    ligand: str = Field(description=f"Ligand to use. The choices are {', '.join(design_space['ligand'])}")
    reagent: str = Field(description=f"Reagent to use. The choices are {', '.join(design_space['reagent'])}")
    solvent: str = Field(description=f"Solvent to use. The choices are {', '.join(design_space['solvent'])}")

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
