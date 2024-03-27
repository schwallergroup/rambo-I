import dspy
from pydantic import BaseModel, Field
from dspy.functional import TypedPredictor
from typing import List

class RetrievalInput(BaseModel):
    """Input for the retrieval module."""
    reaction_class: str = Field(description="The reaction class.")
    keyword_std: str = Field(description="The standard keyword.")
    reaction_group: str = Field(description="The reaction group.")
    rxn_smiles: str = Field(description="The reaction SMILES.")
    product_structure: str = Field(description="The product structure.")
    product_yield_pct_area_uv: float = Field(description="The product yield percentage.")
    solvent_1_name: str = Field(description="The name of the solvent.")
    reaction_t: float = Field(description="The reaction temperature.")
    reaction_time_hrs: float = Field(description="The reaction time in hours.")
    catalyst_1_eq: float = Field(description="The first catalyst equivalent.")
    catalyst_1_id_1_smiles: str = Field(description="The first catalyst ID 1 SMILES.")
    catalyst_1_id_2_smiles: str = Field(description="The first catalyst ID 2 SMILES.")
    catalyst_1_short_hand: str = Field(description="The first catalyst shorthand.")
    catalyst_2_eq: float = Field(description="The second catalyst equivalent.")
    catalyst_2_id_1_smiles: str = Field(description="The second catalyst ID 1 SMILES.")
    catalyst_2_id_2_smiles: str = Field(description="The second catalyst ID 2 SMILES.")
    catalyst_2_short_hand: str = Field(description="The second catalyst shorthand.")
    reactant_1_eq: float = Field(description="The first reactant equivalent.")
    reactant_1_smiles: str = Field(description="The first reactant SMILES.")
    reactant_2_eq: float = Field(description="The second reactant equivalent.")
    reactant_2_smiles: str = Field(description="The second reactant SMILES.")
    reactant_3_eq: float = Field(description="The third reactant equivalent.")
    reactant_3_smiles: str = Field(description="The third reactant SMILES.")
    reagent_1_eq: float = Field(description="The first reagent equivalent.")
    reagent_1_short_hand: str = Field(description="The first reagent shorthand.")
    reagent_2_eq: float = Field(description="The second reagent equivalent.")
    reagent_2_short_hand: str = Field(description="The second reagent shorthand.")

def create_text(row):
    text_parts = []
    text_parts.append(f"The reaction is classified under {row.reaction_class} with a standard keyword of {row.keyword_std}" if row.reaction_class and row.keyword_std else "")
    text_parts.append(f"and belongs to the {row.reaction_group} group." if row.reaction_group else "")
    text_parts.append(f"The reaction between {row.reactant_1_smiles} (equivalent of {row.reactant_1_eq}) and {row.reactant_2_smiles} (equivalent of {row.reactant_2_eq})," if row.reactant_1_smiles and row.reactant_1_eq and row.reactant_2_smiles and row.reactant_2_eq else "")
    text_parts.append(f"is catalyzed by {row.catalyst_1_short_hand} ([{row.catalyst_1_id_1_smiles}, {row.catalyst_1_id_2_smiles}], {row.catalyst_1_eq} equivalents)" if row.catalyst_1_short_hand and row.catalyst_1_id_1_smiles and row.catalyst_1_id_2_smiles and row.catalyst_1_eq else "")
    text_parts.append(f"and {row.catalyst_2_short_hand} ([{row.catalyst_2_id_1_smiles}, {row.catalyst_2_id_2_smiles}], {row.catalyst_2_eq} equivalents)," if row.catalyst_2_short_hand and row.catalyst_2_id_1_smiles and row.catalyst_2_id_2_smiles and row.catalyst_2_eq else "")
    text_parts.append(f"with {row.solvent_1_name} as the solvent." if row.solvent_1_name else "")
    text_parts.append(f"The reaction proceeds at {row.reaction_t}°C for {row.reaction_time_hrs} hours." if row.reaction_t and row.reaction_time_hrs else "")
    text_parts.append(f"The product obtained, {row.product_structure}, has a structure represented by {row.rxn_smiles} for the reaction and {row.product_yield_pct_area_uv}% yield as measured by UV area percent." if row.product_structure and row.rxn_smiles and row.product_yield_pct_area_uv else "")
    return ' '.join(filter(None, text_parts))

class RetrievalSignature(dspy.Signature):
    """Convert the language input into a query similar to the databse."""

    context = dspy.InputField(desc="Relevant conditions used in other reactions found in the literature.")
    query = dspy.InputField(desc="User query, specifies problem and constraints.")
    conditions: List[RetrievalInput] = dspy.OutputField(desc="Initial conditions to start BO.")



def restructure_prompt(prompt: str):
    """Restructure the prompt for the RAG module.

    Args:
        prompt: The input prompt.

    Returns:
        The restructured prompt.
    """

    predictor = TypedPredictor(RetrievalSignature)
    context = "Please convert input"
    
    pred = predictor(context=context, query=prompt)
    # print(pred)

    # Use if we use the text-embedded vector db
    # pred_in_text = create_text(pred.conditions[0])
    # print(pred_in_text)
    return pred

def retrieve_reactions(restructured_prompt: str):
    """Retrieve reactions using the RAG module.

    Args:
        restructured_prompt: The restructured prompt.

    Returns:
        The retrieved reactions.
    """
    # Use RAG in modules.py?
    pass