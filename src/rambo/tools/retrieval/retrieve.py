import dspy
from typing import List

import dspy
from pydantic import BaseModel, Field


class RAGSignature(dspy.Signature):
    """Retrieve conditions used in other similar (successful) reactions in the literature."""

    query: str = dspy.InputField(
        desc="User's query. The query specifies the problem and constraints."
    )
    n: str = dspy.InputField(desc="Retrieve top n conditions.")
    relevant_syntheses: List[str] = dspy.OutputField(
        desc="Summary of conditions used in other relevant reactions."
    )

class ReActRetrieve(dspy.Module):
    def __init__(self, n: int = 5):
        super().__init__()
        self.n = str(n)
        self.react = dspy.ReAct(RAGSignature)
        self.retrieve = dspy.Retrieve(k=n)

    def forward(self, query):
        """Forward pass of the ReActRetrieve module."""
        ctxt = self.retrieve(query)
        return "\n".join(ctxt.passages)

        # response = self.react(query=query, n=self.n)
        # print(response)
        # return response.relevant_syntheses
