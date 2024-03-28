from typing import List, Optional, Union
from pydantic import BaseModel, Field, field_validator
import itertools
import pandas as pd
import numpy as np


class Parameter(BaseModel):
    name: str
    smiles: Optional[List[str]] = None
    values: Optional[List[float]] = None

    @field_validator("smiles", "values")
    def check_non_empty(cls, v):
        if isinstance(v, list) and not v:
            raise ValueError("List must not be empty")
        return v


class DesignSpaceConfig(BaseModel):
    parameters: List[Parameter]


class Design:
    def __init__(
        self,
        design_space_path: str = None,
        design_space_config: DesignSpaceConfig = None,
        objective: str = "yield",
    ) -> None:
        self.path = design_space_path
        self.config = design_space_config
        self.objective = objective
        self.space = self.generate_design_space()

    def generate_design_space(self) -> pd.DataFrame:
        if self.path:
            df = pd.read_csv(self.path)
            df = df.fillna("")
            design_space = df.loc[
                :, [param.name for param in self.config.parameters]
            ].copy()
            design_space.loc[:, self.objective] = df[self.objective]
        else:
            params_dict = {
                param.name: param.smiles if param.smiles else param.values
                for param in self.config.parameters
            }
            all_combinations = list(itertools.product(*params_dict.values()))
            design_space = pd.DataFrame(
                all_combinations, columns=params_dict.keys()
            )
            design_space.loc[:, self.objective] = []
        return design_space

    def query_objective(self, input_point):
        input_params = input_point.conditions[0].model_dump()
        mask = pd.Series([True] * len(self.space))
        for param_name, param_value in input_params.items():
            if param_name in self.space.columns:
                mask &= self.space[param_name] == param_value

        filtered_space = self.space[mask]

        if not filtered_space.empty:
            return filtered_space[self.objective].iloc[0]
        else:
            return "No matching entry found."


def get_design_space(
    design_space_dataset_name: str = "data/suzuki-miyaura.csv",
    param_names: List[str] = [
        "reactant_1",
        "reactant_2",
        "catalyst",
        "ligand",
        "reagent",
        "solvent",
    ],
) -> DesignSpaceConfig:
    design_space = pd.read_csv(design_space_dataset_name)
    design_space = design_space.fillna("")

    parameters = [
        Parameter(name=col, smiles=design_space[col].unique())
        for col in design_space[param_names].columns
    ]

    return {param.name: param.smiles for param in parameters}
