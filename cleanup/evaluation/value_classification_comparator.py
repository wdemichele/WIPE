from typing import Dict
from src.evaluation.value_classification_ground_truth import ValueClassificationGroundTruth
from src.value_adding_analysis.value_classification_gpt_response import ValueClassificationGPTResponse


class ValueClassificationComparator:
    def __init__(self, ground_truth: ValueClassificationGroundTruth, gpt_response: ValueClassificationGPTResponse):
        self.ground_truth = ground_truth
        self.gpt_response = gpt_response

    def compare(self) -> Dict:
        total_activities = len(self.ground_truth.activities)
        correct_classifications = 0
        misclassifications = []

        for gt_activity in self.ground_truth.activities:
            gpt_classification = next(
                (c for c in self.gpt_response.classifications if c['step'] == gt_activity.step),
                None
            )

            if gpt_classification and gpt_classification['category'].value == gt_activity.classification:
                correct_classifications += 1
            else:
                misclassifications.append({
                    'step': gt_activity.step,
                    'ground_truth': gt_activity.classification,
                    'gpt_classification': gpt_classification['category'] if gpt_classification else 'Not classified'
                })

        accuracy = correct_classifications / total_activities if total_activities > 0 else 0

        return {
            'accuracy': accuracy,
            'correct_classifications': correct_classifications,
            'total_activities': total_activities,
            'misclassifications': misclassifications
        }