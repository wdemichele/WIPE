from src.common.util.gpt import GPT
from config import configuration
import json

class MermaidSyntaxCorrectionGPT(GPT):
    def __init__(self, 
                model: str = configuration["openai_model"], 
                api_version: str = configuration["openai_api_version"]
                ):
        super().__init__(model=model, api_version=api_version)
        
        
    def generate_system_message(self):
        return """You are a mermaid code syntax expert that takes as input broken mermaid code and corrects it."""

    def generate_user_message(self, mermaid_code):
        user_message = (
            f"The following is the generated mermaid code that compiled with syntax errors\n\n"
            f"Mermaid code :\n{mermaid_code}"
        )
        return user_message
    
    def correct_mermaid_code(self, mermaid_code, verbose=False) -> dict: 
        gpt_request = self.generate_request(mermaid_code=mermaid_code)
        gpt_response = self.get_gpt_response(gpt_request, verbose=verbose)
        
        return gpt_response