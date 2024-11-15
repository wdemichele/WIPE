from src.common.util.gpt import GPT
from config import configuration

class ValueContextGPT(GPT):  
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):  
        
        super().__init__(model=model, api_version=api_version)
  
    def generate_system_message(self):
        return """You are an AI assistant specialized in analyzing Business Process Model and Notation (BPMN) diagrams to derive essential business and customer values. Your task is to examine the process flow and provide a concise context that will be used for further waste optimization analysis. Follow these guidelines:

        1. Analyze the BPMN diagram to understand the overall process flow.

        2. Identify the primary business values:
        - What is the main objective of this process for the business?
        - What key outcomes does the business aim to achieve through this process?

        3. Determine the core customer values:
        - What primary need or problem does this process address for the customer?
        - What key benefits does the customer receive from this process?

        4. Synthesize the information into two brief context paragraphs:
        - Summarize the business and customer values in 3-5 sentence paragraphs each.
        - Ensure the context is clear and relevant for subsequent waste analysis.

        5. Output Format:
        Provide your analysis in the following format:
        ```
        Business Context:
        [Your 3-5 sentence summary here]
        
        Customer Context:
        [Your 3-5 sentence summary here]
        ```

        Remember, your output will be used in chain-of-thought prompting for waste optimization. Keep your context focused on values that will be relevant for identifying and eliminating waste in the process."""            
    
    def generate_user_message(self, bpmn_text):
        user_message = (
            "Analyze the following BPMN diagram text to derive the essential business "
            "and customer values. Provide brief context paragraphs (3-5 sentences) "
            "for each of business and customer values. This context will be used for subsequent "
            "waste optimization analysis.\n\n"
            f"BPMN diagram text:\n{bpmn_text}"
        )
        return user_message
    
    def bmpn_value_context(self, bpmn_text, verbose=False) -> dict: 
        
        gpt_request = self.generate_request(bpmn_text=bpmn_text)
  
        gpt_response = self.get_gpt_response(gpt_request, verbose=verbose) 
        
        return gpt_response