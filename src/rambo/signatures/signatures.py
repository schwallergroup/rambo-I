import dspy
from pydantic import BaseModel, Field
from typing import List

class RAGSignature(dspy.Signature):
    """Retrieve conditions used in other similar (successful) reactions in the literature."""

    query: str = dspy.InputField(desc="User's query. The query specifies the problem and constraints.")
    n: str = dspy.InputField(desc="Retrieve top n conditions.")
    relevant_syntheses: List[str] = dspy.OutputField(desc="Summary of conditions used in other relevant reactions.")
