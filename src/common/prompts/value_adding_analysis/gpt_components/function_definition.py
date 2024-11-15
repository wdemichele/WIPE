# File: function_definition_variations.py

FUNCTION_DEFINITIONS = {
    "basic": """
    Use the following function to classify each step:

    classify(classification, activity, step, justification)

    Parameters:
    - classification: The type of classification for the step ("VA", "BVA", or "NVA")
    - activity: The name of the activity this step belongs to
    - step: A short, descriptive name for the step
    - justification: The reason for its classification
    """,

    "detailed": """
    Use the following function to classify each step:

    classify(classification: str, activity: str, step: str, justification: str) -> None

    Parameters:
    - classification (str): The type of classification for the step. 
      Must be one of the following:
      * "VA" for Value Adding
      * "BVA" for Business Value Adding
      * "NVA" for Non-Value Adding
    - activity (str): The name of the activity this step belongs to. 
      Use the exact activity name as provided in the input JSON.
    - step (str): A short, descriptive name for the step. 
      Use the step description as provided in the input JSON.
    - justification (str): A brief explanation (1-2 sentences) for why this 
      classification was chosen. Be specific and relate to the step's function.

    Note: This function doesn't return a value. It's used to structure your output.
    """
}