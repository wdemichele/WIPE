from openai import AzureOpenAI
from config import configuration
from pprint import pprint
import regex
import json
import ast 
import re

class GPT:  
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"], api_key=configuration["openai_api_key"], azure_endpoint = configuration["azure_openai_endpoint"], temperature=0.05):  
        
        self.model = model or configuration["openai_model"]
        
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
        
        self.client = AzureOpenAI(
            api_key=api_key,
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint
        )
        
        self.temperature = temperature
  
    def generate_request(self, *args, **kwargs) -> list:
        system_message = self.generate_system_message()
        user_message = self.generate_user_message(*args, **kwargs)

        message_text = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        return message_text
    
    def get_gpt_response(self, message_text: list, response_format= { "type": "text" }, max_tokens=None, verbose=False) -> str:  
        
        chat_completion = self.client.chat.completions.create(  
            messages=message_text,  
            temperature=self.temperature,
            response_format = response_format,
            model=self.model,
            max_tokens = max_tokens
        )  

        result = chat_completion.choices[0].message.content 
        
        if verbose:
            print(result)
        
        return result
    
    def generate_user_message(self, *args, **kwargs):  
        # This method will be implemented by subclasses to send prompts to the GPT model  
        raise NotImplementedError("Subclasses should implement this method.")  
    
    def generate_system_message(self, *args, **kwargs):  
        # This method will be implemented by subclasses to send prompts to the GPT model  
        raise NotImplementedError("Subclasses should implement this method.")  

    def convert_gpt_response_format(self, gpt_response: str) -> dict:  
        
        # Helper function to attempt to parse with json.loads first, then fall back to ast.literal_eval  
        def try_parse_string(data_str: str):  
            try:  
                return json.loads(data_str)  
            except json.JSONDecodeError:  
                try:  
                    return ast.literal_eval(data_str)  
                except (SyntaxError, ValueError):  
                    pass  
            return None  
    
        # Try parsing the entire response as JSON or literal  
        response_dict = try_parse_string(gpt_response)  
        if isinstance(response_dict, dict):  
            return response_dict  
    
        # Try using regular expressions to find JSON-like strings and parse them  
        for pattern in [r'\{(?:[^{}]|(?R))*\}']: # , r'^\{$.*^\}$', r'\{.*\}']:  
            match = regex.search(pattern, gpt_response, re.DOTALL | re.MULTILINE)  
            if match:  
                response_dict = try_parse_string(match.group(0))  
                if isinstance(response_dict, dict):  
                    return response_dict  
    
        # If all methods fail, raise an exception with the GPT response  
        raise ValueError(f"Unable to convert GPT response to a dictionary. Response: {gpt_response}")