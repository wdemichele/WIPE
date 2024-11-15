from src.common.util.gpt import GPT
from config import configuration
import json
from openai import APITimeoutError
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

class ValueClassificationStepLevelGPT(GPT):  
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):  
        super().__init__(model=model, api_version=api_version)
  
    def generate_system_message(self):
        return """You are an AI assistant designed to convert JSON-formatted BPMN analysis output into structured function calls. Your task is to parse the JSON input and create appropriate function calls for each classified step in the process, including the activity it belongs to. Use the following guidelines:

            1. Function Definitions:
            There is a function corresponding to classifying the value adding type for each step:

            classify(classification, activity, step, justification)

            Each function takes the following parameters:
            - classification: The type of classification for the step (string)
                - Value adding: "VA"
                - Business value adding: "BVA"
                - Non-value adding: "NVA"
            - activity: The name of the activity this step belongs to (string)
            - step: A short, descriptive name for the step (string)
            - justification: The reason for its classification (string)

            2. Parsing Instructions:
            - Parse the JSON input to extract each activity and its associated substeps.
            - For each substep, create the appropriate function call based on its classification.
            - Use the provided classification and reasoning for each substep.

            3. Output Format:
            Generate Python-like function calls for each classified step. Each function call should be on a new line.

            Example output:
            ```python
            classify("VA", "Submit equipment rental request", "Fill out rental form", "Directly contributes to meeting customer needs by providing necessary information.")
            classify("BVA", "Submit equipment rental request", "Attach documents", "Necessary for the business to process the request but doesn't directly add value for the customer.")
            classify("VA", "Submit equipment rental request", "Submit request", Directly contributes to meeting customer needs by initiating the rental process.")
            ```

            Your task is to analyze the given JSON input and convert each classified step into the appropriate function call following this format."""            
    
    def generate_user_message(self, json_input):
        user_message = (
            "Convert the following JSON-formatted BPMN analysis output into appropriate function calls "
            "for classify, classifying each step as value adding, business value adding, or non-value adding. "
            "Extract the classification, activity name, step name, and reasoning for each step. "
            "Ensure that the activity name matches activity_name in the input. Ensure that step name matches the step description.\n\n"
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