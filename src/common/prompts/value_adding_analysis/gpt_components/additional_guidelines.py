# File: additional_guidelines_variations.py

ADDITIONAL_GUIDELINES = {
    "context_aware": """
    When classifying steps, consider the following additional guidelines:

    1. Context is crucial: A step's classification may depend on its position in the overall process. 
       What seems non-value adding in isolation might be necessary when considering the bigger picture.

    2. Customer perspective: Always try to view the process from the customer's point of view. 
       What they perceive as valuable should guide your VA classifications.

    3. Industry standards: Some steps might be BVA due to industry regulations or standards, 
       even if they don't directly add value for the customer.

    4. Potential for improvement: When classifying NVA steps, consider if they could be eliminated 
       or combined with other steps to improve efficiency.

    5. Consistency: Ensure similar steps across different activities are classified consistently 
       unless there's a clear reason for differentiation.
    """,

    "lean_principles": """
    When classifying steps, keep in mind the following Lean principles:

    1. Identify value: Classify as VA only those steps that directly contribute to what the customer 
       is willing to pay for.

    2. Map the value stream: Consider how each step fits into the overall flow of value creation. 
       Some BVA steps might be crucial for enabling VA steps.

    3. Create flow: Steps that cause delays or interruptions in the process flow should be 
       scrutinized and potentially classified as NVA.

    4. Establish pull: Steps that are performed "just-in-time" based on actual demand tend to be 
       more value-adding than those done in anticipation of demand.

    5. Seek perfection: Always consider if there's a way to convert BVA or NVA steps into VA steps, 
       or to eliminate NVA steps entirely.

    6. Respect for people: Remember that some steps might seem NVA but are crucial for employee 
       well-being or safety, which indirectly benefits the customer through better service.
    """
}