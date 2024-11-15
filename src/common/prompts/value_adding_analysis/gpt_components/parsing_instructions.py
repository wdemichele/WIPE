# File: parsing_instructions_variations.py

PARSING_INSTRUCTIONS = {
    "sequential": """
    To parse the input JSON and generate the appropriate function calls:

    1. Read through the JSON input sequentially.
    2. For each activity in the JSON:
       a. Extract the activity name.
       b. For each substep in the activity:
          i. Extract the step description.
          ii. Determine the appropriate classification (VA, BVA, or NVA).
          iii. Formulate a brief justification for the classification.
          iv. Create a classify() function call with these elements.
    3. Ensure each function call is on a new line in your output.
    """,

    "holistic": """
    To parse the input JSON and generate the appropriate function calls:

    1. First, review the entire JSON input to understand the full context of the process.
    2. Identify the main activities and their relationships within the process.
    3. For each activity:
       a. Consider how it fits into the overall process flow.
       b. Examine each substep within the context of both its activity and the entire process.
       c. For each substep:
          i. Determine its classification based on its contribution to the activity and the overall process.
          ii. Formulate a justification that considers the substep's role in the broader context.
          iii. Create a classify() function call, ensuring the activity name and step description match the input exactly.
    4. After classifying all substeps, review your classifications for consistency across the entire process.
    5. Output the classify() function calls, each on a new line.
    """
}