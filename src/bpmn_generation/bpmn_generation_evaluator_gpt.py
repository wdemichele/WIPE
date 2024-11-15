import base64
import requests
from config import configuration
import re
from requests.exceptions import ConnectionError, RequestException
import time

class BPMNGenerationEvaluatorGPT:
    def __init__(self):
        self.API_KEY = configuration.get('gpt_4o_openai_api_key')
        self.ENDPOINT = "https://algo-gpt-3-turbo.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }

    def encode_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('ascii')

    def create_message_content(self, original_image, generated_image):
        return [
            {
                "type": "text",
                "text": """Compare these two BPMN diagrams. The first is the original, and the second is generated from Mermaid code. Your task is to determine if they are structurally equivalent.

            Instructions:
            1. Ignore formatting differences such as layout, colors, or exact shapes used for nodes.
            2. Focus on significant structural differences that affect the process flow or logic.
            3. Consider the following as equivalent:
            - Different representations of the same type of gateway (e.g., 'XORGateway' vs. 'X' for exclusive gateway and 'ParallelGateway' vs. '+' for parallel gateway)
            - Minor differences in node labels that don't change the meaning
            - Slight variations in the order of parallel tasks

            4. Consider the following as non-equivalent:
            - Missing or extra nodes
            - Different types of gateways used (e.g., exclusive vs. parallel)
            - Changes in the flow logic or sequence of tasks
            - Significant differences in node labels that alter the meaning of the task

            5. If the diagrams are structurally equivalent, respond with:
            <<EQUIVALENT>>
            Briefly explain why they are considered equivalent.

            6. If the diagrams are not structurally equivalent, respond with:
            <<NOT EQUIVALENT>>
            Then, provide a concise list of significant structural differences. For each difference:
            a) Describe the specific element in the original diagram
            b) Describe how it differs in the Mermaid-generated diagram
            c) Suggest a high-level modification to make the Mermaid version match the original

            Do not provide Mermaid code in your response. Only give textual descriptions of the differences and suggested modifications.

            Remember, minor aesthetic differences or slight variations that don't affect the overall process flow should not be considered as making the diagrams non-equivalent. I am only interested in ensuring the Mermaid code is a structurally equivalent representation of the originalBPMN diagram. Give your structural equivalence decision at the very end of your message, after you have analysed both diagrams thoroughly."""
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{original_image}"
                }
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{generated_image}"
                }
            }
        ]

    def create_payload(self, message_content, temperature=0.4, top_p=0.95, max_tokens=1000):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }

    def send_request(self, payload, max_retries=3, retry_delay=5):
        retries = 0
        while retries <= max_retries:
            try:
                response = requests.post(self.ENDPOINT, headers=self.headers, json=payload, verify=True)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
            
            except ConnectionError as ce:
                print(f"ConnectionError occurred: {ce}")
                retries += 1
                if retries <= max_retries:
                    print(f"Retrying in {retry_delay} seconds... (Attempt {retries} of {max_retries})")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Unable to establish connection.")
                    return None
            
            except RequestException as e:
                print(f"An error occurred: {e}")
                if response is not None:
                    print(f"Response status code: {response.status_code}")
                    print(f"Response content: {response.text}")
                return None
            
    def suggest_revisions(self):
        revision_instructions = """You will now be instructing another GPT to make the necessary changes to their mermaid code generation. Please concisely communicate the changes needed to get the two BPMN diagrams to be structurally equivalent. Remember to focus on significant structural differences that affect the process flow or logic. Remember the first image is the actual BPMN diagram, and the second image is the one generated from the Mermaid code. Do not provide Mermaid code in your response. Only give textual descriptions of the differences and suggested modifications."""
        return revision_instructions

    def evaluate_bpmn(self, original_image_path, generated_image_path):
        original_image = self.encode_image(original_image_path)
        generated_image = self.encode_image(generated_image_path)
        message_content = self.create_message_content(original_image, generated_image)
        payload = self.create_payload(message_content)
        result = self.send_request(payload)
        
        if result:
            is_equivalent = "<<EQUIVALENT>>" in result
            description = re.sub(r'<<(NOT )?EQUIVALENT>>', '', result).strip()
            
            if is_equivalent:
                return is_equivalent, description
            
            # append a new message to payload to get the revisions
            payload['messages'].append({
                "role": "assistant",
                "content": result
            })
            payload['messages'].append({
                "role": "user",
                "content": self.suggest_revisions()
            })
            revisions = self.send_request(payload)
            
            return is_equivalent, revisions
        else:
            return None, None
