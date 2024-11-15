from src.common.util.gpt import GPT
from config import configuration
import json
from typing import List, Dict

class ActivityBreakdownComparatorGPT(GPT):
    def __init__(self, model=configuration["openai_model"], api_version=configuration["openai_api_version"]):
        super().__init__(model=model, api_version=api_version)

    def generate_system_message(self):
        return """You are an AI assistant specialized in comparing and mapping steps in business processes. Your task is to analyze the ground truth steps and the response steps for a given business process activity, determine the best mappings between steps based on semantic similarity, and provide a structured output of the relationships. Follow these guidelines:

        1. **Step Matching**:

            a. **Comprehensive Comparison**: Compare each ground truth step with each response step within the same activity.

            b. **Semantic Analysis**: Determine the best matches based on semantic similarity, considering synonyms, paraphrasing, context, and domain-specific terminology.

            c. **Handling Granularity**: Recognize that some steps may be more granular than others. A single ground truth step may correspond to multiple response steps, and vice versa.

            d. **Step Grouping**: If a ground truth step matches multiple response steps (or vice versa), group them together in the mapping.

        2. **Matching Criteria**:

            a. **Match Types**: For each matched pair or group, assign a **match type**:

                - Identical Match

                Steps are identical or nearly identical in wording and meaning.
                Example: "Send email to client" vs "Send outreach email to client"

                - Functional Equivalence

                Steps describe the same action or outcome using different words. The core function is identical, even if the specific method might vary slightly.
                Example: "Dispatch product to customer" vs "Ship item to buyer"

                - Granularity Difference

                Steps share some common elements but differ significantly in scope or granularity.
                This category covers cases where steps partially overlap or where one step might encompass multiple steps in the other decomposition.
                Example: "Conduct meeting" vs "1. Set up conference call, 2. Lead discussion, 3. Summarize action items"

                - No Match

                Steps do not correspond to each other in any meaningful way.
                This category is used when a step in one decomposition has no relatable step in the other.
                Example: "Update CRM system" vs "Prepare presentation slides" (assuming these are from the same part of the process in different decompositions)
                            
            b. **Confidence Score**: Assign a **confidence score** (0-100) reflecting the degree of similarity.

        3. **Order and Sequence**:

            a. **Step Numbers**: Include the original step numbers from both the ground truth and response.

            b. **Sequence Analysis**: Note if the matched steps are in the same order or if there are significant sequencing differences.

        4. **Unmatched Steps**:

            a. **Identification**: List any steps in the ground truth or response that do not have a corresponding match.

            b. **Explanations**: Provide brief explanations for why these steps are unmatched.

        5. **Output Structure**:

            Provide your analysis in a JSON format as follows:

            ```json
            {
                "activity_name": "Name of the activity",
                "step_mappings": [
                    {
                        "ground_truth_steps": [
                            {
                                "step_number": X,
                                "description": "Ground truth step description"
                            },
                            ...
                        ],
                        "response_steps": [
                            {
                                "step_number": Y,
                                "description": "Response step description"
                            },
                            ...
                        ],
                        "match_type": "Identical Match" | "Functional Equivalence" | "Granularity Difference" | "No Match",
                        "confidence": 85,
                        "explanation": "Brief explanation of the match or mismatch"
                    },
                    ...
                ],
                "unmatched_ground_truth_steps": [
                    {
                        "step_number": X,
                        "description": "Ground truth step description",
                        "reason": "Explanation of why this step is unmatched"
                    },
                    ...
                ],
                "unmatched_response_steps": [
                    {
                        "step_number": Y,
                        "description": "Response step description",
                        "reason": "Explanation of why this step is unmatched"
                    },
                    ...
                ],
                "overall_similarity_score": 0-100,
                "missing_steps_explanation": "Explanation if steps are missing in ground truth or response"
            }
            ```

        6. **Granularity Differences**:

            a. **Grouping Steps**: When handling differences in granularity, group related steps together.

            b. **Detailed Explanations**: Indicate in your explanation when and why steps have been grouped due to granularity differences.

        7. **Formatting Guidelines**:

            - Ensure the JSON output is well-structured and properly formatted.

            - Do not include any additional text outside the JSON structure.

        8. **Example (for illustration purposes)**:

            ```json
            {
                "activity_name": "Example Activity",
                "step_mappings": [
                    {
                        "ground_truth_steps": [
                            {
                                "step_number": 1,
                                "description": "Ground truth step 1"
                            }
                        ],
                        "response_steps": [
                            {
                                "step_number": 1,
                                "description": "Response step 1"
                            },
                            {
                                "step_number": 2,
                                "description": "Response step 2"
                            }
                        ],
                        "match_type": "Granularity Difference",
                        "confidence": 90,
                        "explanation": "Ground truth step 1 corresponds to response steps 1 and 2."
                    }
                ],
                "unmatched_ground_truth_steps": [],
                "unmatched_response_steps": [],
                "overall_similarity_score": 90,
                "missing_steps_explanation": ""
            }
            ```
        """


    def generate_user_message(self, ground_truth: dict, response: dict):
        return f"""Compare the following ground truth activity and substeps with the response activity and substeps. Provide a detailed mapping of steps, identifying matches and non-matches, along with match types, confidence scores, and explanations, as specified in the system message.

            Ground Truth:
            {json.dumps(ground_truth, indent=2)}

            Response:
            {json.dumps(response, indent=2)}

            Please provide your analysis in the JSON format specified in the system message.
            """


    def compare_activity_breakdown(self, activity_ground_truth: dict, activity_generation: dict, verbose=False) -> dict:
        gpt_request = self.generate_request(ground_truth=activity_ground_truth, response=activity_generation)
        gpt_response = self.get_gpt_response(gpt_request, verbose=verbose)
        return self.convert_gpt_response_format(gpt_response)