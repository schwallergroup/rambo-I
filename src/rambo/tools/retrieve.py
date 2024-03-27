import dspy

from ..signatures import RAGSignature


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
