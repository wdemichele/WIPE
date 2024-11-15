from src.common.util.gpt import GPT
from config import configuration
import concurrent.futures
from typing import Optional
from src.common.prompts.activity_breakdown.prompt_components import ABPromptComponents

from dataclasses import asdict

class ActivityBreakdownComponentsGPT(GPT):
    def __init__(self, 
                prompt_components: Optional[ABPromptComponents] = None,
                model: str = configuration["openai_model"], 
                api_version: str = configuration["openai_api_version"]):
        super().__init__(model=model, api_version=api_version)
        
        # Initialize with default empty values
        self.prompt_components = {
            'role_description': "",
            'task_description': "",
            'guidelines': "",
            'output_format': "",
            'example_output': "",
            'focus_shift': "",
        }
        
        # If PromptComponents is provided, update the prompt_components
        if prompt_components:
            self.update_prompt_components(prompt_components)

    def update_prompt_components(self, prompt_components: ABPromptComponents):
        """
        Update the prompt components with values from a PromptComponents object.
        """
        components_dict = asdict(prompt_components)
        for key, value in components_dict.items():
            if value is not None:
                self.prompt_components[key] = value

    def generate_system_message(self):
        return f"""
    {self.prompt_components['role_description']}

    {self.prompt_components['task_description']}

    {"Guidelines for your responses:" if self.prompt_components['guidelines'] else ""}
    {self.prompt_components['guidelines']}

    {"Focus Shift:" if self.prompt_components['focus_shift'] else ""}
    {self.prompt_components['focus_shift']}

    {"Output Format:" if self.prompt_components['output_format'] else ""}
    {self.prompt_components['output_format']}

    {"Example Output:" if self.prompt_components['example_output'] else ""}
    {self.prompt_components['example_output']}
    """

    def generate_user_message(self, bpmn_text):
        user_message = f"""Analyze the following BPMN diagram text and break down each activity in the business process into its constituent substeps.

        For each activity in the process:
        1. Identify the activity name.
        2. Break it at most 3-5 substeps. Not every activity will need to be broken down to substeps.
        3. Ensure each substep is described briefly and concisely (maximum 10 words).
        4. Focus on actionable, specific steps that can be easily observed and measured.

        Provide your analysis as a list of JSON objects, one for each activity in the process, following the structure specified in the system message.

        BPMN diagram text:
        {bpmn_text}

        Please proceed with the breakdown of all activities in this business process."""
        return user_message
    
    def bpmn_activity_breakdown(self, bpmn_text, max_retries=2, verbose=False) -> dict:
        try:
            # First, try processing without chunking
            result = self.process_without_chunking(bpmn_text, verbose)
            if result:
                return result
            
            # If processing without chunking fails, fall back to chunking
            return self.process_with_chunking(bpmn_text, max_retries, verbose)
        except Exception as e:
            if verbose:
                print(f"Error in bpmn_activity_breakdown: {e}")
            return {}

    def process_without_chunking(self, bpmn_text, verbose=False):
        try:
            gpt_request = self.generate_request(bpmn_text=bpmn_text)
            response = self.get_gpt_response(gpt_request, verbose=verbose)
            return self.convert_gpt_response_format(response)["activity_breakdown"]
        except Exception as e:
            if verbose:
                print(f"Error processing without chunking: {e}")
            return None

    def process_with_chunking(self, bpmn_text, max_retries=2, verbose=False):
        def process_chunk(chunk):
            try:
                gpt_request = self.generate_request(bpmn_text=chunk)
                response = self.get_gpt_response(gpt_request, verbose=verbose)
                return self.convert_gpt_response_format(response)["activity_breakdown"]
            except Exception as e:
                if verbose:
                    print(f"Error processing chunk: {e}")
                return None

        def recursive_process(text, depth=0):
            if depth >= max_retries:
                raise Exception("Max retries reached, unable to process BPMN text")
            result = process_chunk(text)
            if result is not None:
                return result
            # If processing failed, split the text and try again
            lines = text.split('\n')
            mid = len(lines) // 2
            left_chunk = '\n'.join(lines[:mid])
            right_chunk = '\n'.join(lines[mid:])
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                future_left = executor.submit(recursive_process, left_chunk, depth + 1)
                future_right = executor.submit(recursive_process, right_chunk, depth + 1)
                result_left = future_left.result()
                result_right = future_right.result()
            return result_left + result_right

        return recursive_process(bpmn_text)