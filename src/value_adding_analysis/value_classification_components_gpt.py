from src.common.util.gpt import GPT
from config import configuration
import json
from openai import APITimeoutError
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional
from src.common.prompts.value_adding_analysis.gpt_components import VAPromptComponents

from dataclasses import asdict

class ValueClassificationComponentsGPT(GPT):
    def __init__(self, 
                prompt_components: Optional[VAPromptComponents] = None,
                model: str = configuration["openai_model"], 
                api_version: str = configuration["openai_api_version"]):
        super().__init__(model=model, api_version=api_version)
        
        # Initialize with default empty values
        self.prompt_components = {
            "role_description": "",
            "task_description": "",
            "classification_types": "",
            "function_definition": "",
            "parsing_instructions": "",
            "output_format": "",
            "example_output": "",
            "additional_guidelines": ""
        }
        
        # If PromptComponents is provided, update the prompt_components
        if prompt_components:
            self.update_prompt_components(prompt_components)

    def update_prompt_components(self, prompt_components: VAPromptComponents):
        """
        Update the prompt components with values from a PromptComponents object.
        """
        components_dict = asdict(prompt_components)
        for key, value in components_dict.items():
            if value is not None:
                self.prompt_components[key] = value

    def generate_system_message(self):
        self.system_message = f"""
{self.prompt_components['role_description']}

{self.prompt_components['task_description']}

{"Classification Types:" if self.prompt_components['classification_types'] else ""}
{self.prompt_components['classification_types']}

{"Function Definition:" if self.prompt_components['function_definition'] else ""}
{self.prompt_components['function_definition']}

{"Parsing Instructions:" if self.prompt_components['parsing_instructions'] else ""}
{self.prompt_components['parsing_instructions']}

{"Output Format:" if self.prompt_components['output_format'] else ""}
{self.prompt_components['output_format']}

{"Example Output:" if self.prompt_components['example_output'] else ""}
{self.prompt_components['example_output']}

{"Additional Guidelines:" if self.prompt_components['additional_guidelines'] else ""}
{self.prompt_components['additional_guidelines']}
"""
        return self.system_message

    def generate_user_message(self, json_input):
        user_message = (
            f"{self.prompt_components['task_description']}\n\n"
            f"JSON input:\n{json.dumps(json_input, indent=2)}"
        )
        return user_message
    
    def value_classification_serial_step_level(self, json_input, verbose=False) -> dict: 
        gpt_response = ""
        num_steps = len(json_input)
        max_steps = 5
        for i in range(0, num_steps, max_steps):
            gpt_request = self.generate_request(json_input=json_input[i:i+max_steps])
            gpt_response += self.get_gpt_response(gpt_request, verbose=verbose)
        
        return gpt_response
    
    def value_classification_step_level(self, json_input, multiprocess=False, verbose=False) -> dict:
        num_steps = len(json_input)
        max_steps = 5
        num_batches = math.ceil(num_steps / max_steps)
        batch_size = math.ceil(num_steps / num_batches)

        def process_batch(batch):
            gpt_request = self.generate_request(json_input=batch)
            return self.get_gpt_response(gpt_request, verbose=verbose)

        if multiprocess:
            with ThreadPoolExecutor() as executor:
                futures = []
                for i in range(0, num_steps, batch_size):
                    batch = json_input[i:min(i + batch_size, num_steps)]
                    futures.append(executor.submit(process_batch, batch))

                gpt_responses = []
                for future in as_completed(futures):
                    gpt_responses.append(future.result())
        else:
            gpt_responses = []
            for i in range(0, num_steps, batch_size):
                batch = json_input[i:min(i + batch_size, num_steps)]
                gpt_responses.append(process_batch(batch))

        return ''.join(gpt_responses)