from src.common.util.gpt import GPT
from config import configuration
import concurrent.futures

class ActivityBreakdownGPT(GPT):  
    def __init__(self, prompt_components, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):  
        self.prompt_components = prompt_components
        super().__init__(model=model, api_version=api_version)
  
    def generate_system_message(self):
        return """
        You are an expert in business process analysis and improvement. Your task is to break down business activities into their constituent substeps. These substeps will be used to identify waste and inefficiencies in the process.

        Guidelines for your responses:
        1. Provide your output in JSON format.
        2. Each activity should have no more than 5 substeps.
        3. Describe each substep with a brief, concise sentence (maximum 10 words).
        4. Focus on actionable, specific steps that can be easily observed and measured.
        5. Ensure the substeps cover the entire activity from start to finish.

        Your response should follow this structure:
        {"activity_breakdown" = [
            {
            'activity_name': 'Name of the activity',
            'substeps': [
                {'step_number': 1, 'description': 'Brief description of substep 1'},
                {'step_number': 2, 'description': 'Brief description of substep 2'},
                ...
            ]
            },
        ...
        ]}

        For each activity, break it down following these guidelines. For multiple activities in the business process, create a JSON list of activity breakdown objects."
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