import os
import requests
import base64
import re
from config import configuration

class BPMNGenerationGPT:
    def __init__(self):
        self.API_KEY = configuration.get('gpt_4o_openai_api_key')
        self.ENDPOINT = "https://algo-gpt-3-turbo.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-02-15-preview"
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.API_KEY,
        }
        self.messages = []

    def encode_image(self, image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('ascii')
        
    def get_zero_shot_simple_prompt(self):
        return "Please generate a BPMN mermaid notation from the following image:"

    def get_detailed_instructions_prompt(self):
        return """Please generate a BPMN mermaid notation from the following image. Follow these detailed instructions:

            1. Analyze the image carefully, identifying all BPMN elements including start and end events, tasks, gateways, and flows.

            2. Use the correct Mermaid syntax for BPMN elements:
            - Start event: [<LABEL>]
            - End event: [<LABEL>]
            - Tasks: rectangular nodes with labels
            - Gateways: diamond shapes, use appropriate labels (e.g., {XORGateway} for exclusive, {ParallelGateway} for parallel)
            - Flows: --> for sequence flows, use labels for condition flows

            3. Maintain the exact structure and flow of the diagram:
            - Preserve the order and relationships between all elements
            - Ensure all branches and merges are accurately represented
            - Include all decision points and their corresponding flows
            - You should represent every gateway and flow present in the image

            4. Use clear and concise labels:
            - Keep task names short but descriptive
            - Use the exact text from the image for labels where possible
            - For condition flows, use brief but clear condition labels

            5. Represent parallel processes correctly:
            - Use parallel gateways {ParallelGateway} to split and merge parallel flows
            - Ensure all parallel paths are complete before merging

            6. Handle exclusive gateways properly:
            - Use {XORGateway} for exclusive gateways
            - Label each outgoing flow with its condition

            7. Include any swimlanes or pools if present in the image:
            - Use subgraphs to represent different lanes or pools
            - Ensure tasks are placed in the correct lanes

            8. Pay attention to any special elements or notations in the image and represent them as closely as possible in Mermaid.

            9. Format the Mermaid code for readability:
            - Use proper indentation for nested elements
            - Group related elements together

            10. Enclose the entire Mermaid code in ```mermaid and ``` tags.

            Please generate the Mermaid code based on these instructions, ensuring it accurately represents the BPMN diagram in the image."""
        
    def create_message_content(self, encoded_image):
        return [
            {
                "type": "text",
                "text": self.get_detailed_instructions_prompt()
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]

    def send_request(self, messages, temperature=0.4, top_p=0.95, max_tokens=1000):
        payload = {
            "messages": messages,
            "temperature": temperature,
            # "top_p": top_p,
            "max_tokens": max_tokens
        }
        try:
            response = requests.post(self.ENDPOINT, headers=self.headers, json=payload, verify=True)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            if response is not None:
                print(f"Response status code: {response.status_code}")
                print(f"Response content: {response.text}")
            return None

    def extract_mermaid_code(self, content):
        mermaid_pattern = r'```mermaid\n([\s\S]*?)\n```'
        match = re.search(mermaid_pattern, content)
        if match:
            return match.group(1).strip()
        else:
            print("No Mermaid code found in the response.")
            return content

    def generate_bpmn(self, image_path):
        encoded_image = self.encode_image(image_path)
        message_content = self.create_message_content(encoded_image)
        self.messages.append({"role": "user", "content": message_content})
        
        response = self.send_request(self.messages)
        if response:
            self.messages.append({"role": "assistant", "content": response})
            return self.extract_mermaid_code(response)
        return None

    def revise_bpmn(self, revisions):
        revision_message = f"Please update the mermaid code with these revisions:\n\n{revisions}"
        self.messages.append({"role": "user", "content": revision_message})
        
        response = self.send_request(self.messages)
        if response:
            self.messages.append({"role": "assistant", "content": response})
            return self.extract_mermaid_code(response)
        return None

    def get_message_history(self):
        return self.messages