TASK_DESCRIPTIONS = {
    "standard": """
    Your task is to analyze the given JSON-formatted BPMN process output and classify each step as either 
    value adding (VA), business value adding (BVA), or non-value adding (NVA). For each step, you should:
    1. Determine the appropriate classification based on the step's contribution to the process.
    2. Provide a brief justification for your classification.
    3. Format your response as a function call for each step, including the classification, activity name, 
       step name, and justification.
    """,

    "efficiency_focused": """
    Your task is to evaluate the efficiency of a business process by analyzing the given JSON-formatted BPMN 
    process output. Classify each step as value adding (VA), business value adding (BVA), or non-value adding (NVA), 
    with a focus on identifying potential areas for process improvement. For each step:
    1. Assess its contribution to overall process efficiency.
    2. Classify it based on its value contribution.
    3. Provide a concise explanation for your classification, highlighting any efficiency considerations.
    4. Format your response as a function call for each step, including the classification, activity name, 
       step name, and your efficiency-focused justification.
    """
}