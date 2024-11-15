from src.common.util.gpt import GPT
from config import configuration
import json

class ValueAnalysisStepLevelGPT(GPT):
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):
        super().__init__(model=model, api_version=api_version)

    def generate_system_message(self):
        return """
        You are an expert in business process analysis and value stream mapping. Your task is to analyze the substeps of business activities and classify them according to their value contribution. Use the following guidelines:

        1. Classify each substep as one of the following:
           - Value-Adding (VA): Directly contributes to meeting customer needs or business objectives.
           - Business Value-Adding (BVA): Necessary for the business but doesn't directly add value for the customer.
           - Non-Value-Adding (NVA): Does not contribute to customer value or business needs and could potentially be eliminated.

        2. Provide a brief explanation for each classification (maximum 15 words).

        3. Your output should be in JSON format, maintaining the structure of the input but adding classification and reasoning to each substep.

        Your response should follow this structure:
        [
            {
                "activity_name": "Name of the activity",
                "substeps": [
                    {
                        "step_number": 1,
                        "description": "Brief description of substep",
                        "classification": "VA/BVA/NVA",
                        "reasoning": "Brief explanation for the classification"
                    },
                    ...
                ]
            },
            ...
        ]
        """

    def generate_user_message(self, activities_breakdown):
        user_message = f"""
        Analyze the following breakdown of business process activities and their substeps. For each substep, determine whether it is Value-Adding (VA), Business Value-Adding (BVA), or Non-Value-Adding (NVA). Provide a brief explanation for each classification.

        Use the provided activity breakdown and classify each substep:

        {json.dumps(activities_breakdown, indent=2)}

        Please proceed with the value analysis of all substeps in this business process, maintaining the structure of the input but adding classification and reasoning to each substep.
        """
        return user_message

    def value_analysis_step_level(self, activities_breakdown, verbose=False) -> dict:
        gpt_request = self.generate_request(activities_breakdown=activities_breakdown)
        gpt_response = self.get_gpt_response(gpt_request, verbose=verbose)
        return gpt_response