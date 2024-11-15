from src.common.util.gpt import GPT
from config import configuration

class ValueAnalysisGPT(GPT):  
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):  
        
        super().__init__(model=model, api_version=api_version)
  
    def generate_system_message(self):
        return """You are an AI assistant specialized in analyzing Business Process Model and Notation (BPMN) diagrams. Your task is to identify value-adding and non-value-adding steps in business processes. Follow these guidelines:

            Process Understanding:
            Carefully examine the entire BPMN diagram provided.
            Identify each step, decision point, and flow in the process.
            Understand the context and industry of the process if provided.
            
            Examine the BPMN diagram carefully.
            For each step, determine if it is value-adding or non-value-adding:

            Value-adding: Directly contributes to meeting customer needs or business objectives.
            Non-value-adding: Does not directly contribute to customer value or is redundant.

            Classify steps into three categories:
            a. Value-adding (VA)
            b. Business value-adding (BVA)
            c. Non-value-adding (NVA)
            Provide a concise report:

            List steps by category (VA, BVA, NVA)
            Briefly explain the classification for each step

            Keep your analysis objective and based on process improvement principles. Consider the overall process context when making your assessment."""            
    
    def generate_user_message(self, bpmn_text, value_context_response):
        user_message = (
            "Analyze the following BPMN diagram text for value-adding (VA), "
            "necessary business-value-adding (BVA), and non-value-adding (NVA) steps. "
            "Provide a concise report with step classifications and improvement suggestions.\n\n"
            "You should consider the following business context and customer value proposition:\n"
            f"Business Context and Customer Value Proposition: {value_context_response}\n\n"
            "Now here is the BPMN diagram for you to analyse:\n"
            f"BPMN diagram text:\n{bpmn_text}"
        )
        return user_message
    
    def bmpn_value_analysis(self, bpmn_text, value_context_response, verbose=False) -> dict: 
        
        gpt_request = self.generate_request(bpmn_text=bpmn_text, value_context_response=value_context_response)
  
        gpt_response = self.get_gpt_response(gpt_request, verbose=verbose) 
        
        return gpt_response