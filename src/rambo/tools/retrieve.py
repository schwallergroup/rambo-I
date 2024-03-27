import dspy


def restructure_prompt(prompt: str):
    """Restructure the prompt for the RAG module.

    Args:
        prompt: The input prompt.

    Returns:
        The restructured prompt.
    """
    
    return f"question: {prompt} context: "

def retrieve_reactions(restructured_prompt: str):
    """Retrieve reactions using the RAG module.

    Args:
        restructured_prompt: The restructured prompt.

    Returns:
        The retrieved reactions.
    """
    rag = dspy.RAG()
    return rag(restructured_prompt).answer

def suggest_synthesis(prompt: str):
    """Suggest a synthesis given a prompt.

    Args:
        prompt: The input prompt.

    Returns:
        The suggested synthesis.
    """
    restructured_prompt = restructure_prompt(prompt)
    return retrieve_reactions(restructured_prompt)