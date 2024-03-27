import dspy


class RAG(dspy.Module):
    def __init__(self, num_passages: int = 3):
        """Basic RAG module for question answering.

        Args:
            num_passages: Number of passages to retrieve for each question.
        """
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(
            "question, contexts -> answer"
        )

    def forward(
        self, question: str, initial_context: str = ""
    ) -> dspy.Prediction:
        """Forward pass of the RAG module.

        Args:
            question: The input question.

        Returns:
            A dspy.Prediction object containing the predicted answer.
        """
        contexts = "\n".join(self.retrieve(question).passages)

        print(f"Retrieved contexts: {contexts}")
        prediction = self.generate_answer(question=question, contexts=contexts)
        return dspy.Prediction(answer=prediction.answer)
