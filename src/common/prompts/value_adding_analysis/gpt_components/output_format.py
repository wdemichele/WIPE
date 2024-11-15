# File: output_format_variations.py

OUTPUT_FORMATS = {
    "basic": """
    Format your output as a series of function calls, one per line. Each function call should follow this format:

    classify("CLASSIFICATION", "Activity Name", "Step Description", "Justification for classification")

    Replace CLASSIFICATION with VA, BVA, or NVA as appropriate. Use the exact activity name and step description from the input JSON. Provide a brief justification for each classification.
    """,

    "structured": """
    Format your output as a series of function calls, grouped by activity. Use the following structure:

    # Activity Name
    classify("CLASSIFICATION", "Activity Name", "Step 1 Description", "Justification for classification")
    classify("CLASSIFICATION", "Activity Name", "Step 2 Description", "Justification for classification")
    ...

    # Next Activity Name
    classify("CLASSIFICATION", "Next Activity Name", "Step 1 Description", "Justification for classification")
    classify("CLASSIFICATION", "Next Activity Name", "Step 2 Description", "Justification for classification")
    ...

    Replace CLASSIFICATION with VA, BVA, or NVA as appropriate. Use the exact activity name and step description from the input JSON. Provide a concise but informative justification for each classification.
    """
}