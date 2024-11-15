from dataclasses import dataclass
from typing import List, Dict, Any
from collections import defaultdict
from src.common.models.process_model import ProcessModel
from src.common.models.value_adding_analysis import ValueAddingAnalysis
    
@dataclass
class ValueAddingAnalysisMetrics:
    total_substeps: int
    correct_classifications: int
    accuracy: float
    misclassifications: List[Dict[str, str]]
    confusion_matrix: Dict[str, Dict[str, int]]
    
    def to_dict(self):
        return {
            "total_substeps": self.total_substeps,
            "correct_classifications": self.correct_classifications,
            "accuracy": self.accuracy,
            "misclassifications": self.misclassifications,
            "confusion_matrix": self.confusion_matrix
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            total_substeps=data["total_substeps"],
            correct_classifications=data["correct_classifications"],
            accuracy=data["accuracy"],
            misclassifications=data["misclassifications"],
            confusion_matrix=data["confusion_matrix"]
        )


def compare_value_classifications(gpt_breakdown: ProcessModel, ground_truth: ProcessModel) -> ValueAddingAnalysisMetrics:
    if isinstance(gpt_breakdown, list):
        gpt_breakdown = ValueAddingAnalysis.from_dict("dummy_process", gpt_breakdown)
    
    if isinstance(ground_truth, list):
        ground_truth = ValueAddingAnalysis.from_dict("dummy_process", ground_truth)
    
    total_substeps = 0
    correct_classifications = 0
    misclassifications = []
    confusion_matrix = defaultdict(lambda: defaultdict(int))

    for gpt_activity, gt_activity in zip(gpt_breakdown.activities, ground_truth.activities):
        if gpt_activity.activity_name != gt_activity.activity_name:
            print(f"Warning: Activity mismatch: {gpt_activity.activity_name} vs {gt_activity.activity_name}")
            continue

        # Determine which list is longer (if any)
        gpt_substeps = gpt_activity.substeps
        gt_substeps = gt_activity.substeps
        longer_list = gpt_substeps if len(gpt_substeps) > len(gt_substeps) else gt_substeps
        shorter_list = gt_substeps if len(gpt_substeps) > len(gt_substeps) else gpt_substeps

        i, j = 0, 0
        while i < len(longer_list) and j < len(shorter_list):
            gpt_substep = gpt_substeps[i] if len(gpt_substeps) > len(gt_substeps) else gpt_substeps[j]
            gt_substep = gt_substeps[j] if len(gpt_substeps) > len(gt_substeps) else gt_substeps[i]

            if gpt_substep.description != gt_substep.description:
                print(f"Warning: Substep mismatch in {gpt_activity.activity_name}: {gpt_substep.description} vs {gt_substep.description}")
                # Skip this step in the longer list
                if len(gpt_substeps) > len(gt_substeps):
                    i += 1
                else:
                    j += 1
                continue

            total_substeps += 1
            
            gpt_classification = gpt_substep.classification if gpt_substep.classification else "Unclassified"
            gt_classification = gt_substep.classification if gt_substep.classification else "Unclassified"
            
            confusion_matrix[gt_classification][gpt_classification] += 1

            if gpt_classification == gt_classification:
                correct_classifications += 1
            else:
                misclassifications.append({
                    "activity": gpt_activity.activity_name,
                    "substep": gpt_substep.description,
                    "gpt_classification": gpt_classification,
                    "ground_truth_classification": gt_classification,
                    "gpt_reasoning": getattr(gpt_substep, 'reasoning', None),
                    "ground_truth_reasoning": getattr(gt_substep, 'reasoning', None)
                })

            i += 1
            j += 1

    accuracy = correct_classifications / total_substeps if total_substeps > 0 else 0

    return ValueAddingAnalysisMetrics(
        total_substeps=total_substeps,
        correct_classifications=correct_classifications,
        accuracy=accuracy,
        misclassifications=misclassifications,
        confusion_matrix=dict(confusion_matrix)
    )

def print_comparison_results(metrics: ValueAddingAnalysisMetrics):
    print(f"Total substeps: {metrics.total_substeps}")
    print(f"Correct classifications: {metrics.correct_classifications}")
    print(f"Accuracy: {metrics.accuracy:.2%}")
    print("\nConfusion Matrix:")
    categories = sorted(set(key for subdict in metrics.confusion_matrix.values() for key in subdict.keys()))
    print("    " + " ".join(f"{cat:>5}" for cat in categories))
    for true_cat in categories:
        print(f"{true_cat:>3}", end=" ")
        for pred_cat in categories:
            print(f"{metrics.confusion_matrix.get(true_cat, {}).get(pred_cat, 0):5}", end=" ")
        print()
    
    if metrics.misclassifications:
        print("\nMisclassifications:")
        for misclassification in metrics.misclassifications:
            print(f"Activity: {misclassification['activity']}")
            print(f"Substep: {misclassification['substep']}")
            print(f"GPT Classification: {misclassification['gpt_classification']}")
            print(f"Ground Truth Classification: {misclassification['ground_truth_classification']}")
            print(f"GPT Reasoning: {misclassification['gpt_reasoning']}")
            print(f"Ground Truth Reasoning: {misclassification['ground_truth_reasoning']}")
            print()