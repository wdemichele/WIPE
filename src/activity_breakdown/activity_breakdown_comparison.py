from dataclasses import dataclass
from typing import List, Optional
from src.common.models.process_model import ProcessModel
from src.activity_breakdown import ActivityBreakdownComparatorGPT

@dataclass
class StepMapping:
    ground_truth_step: str
    response_step: str
    confidence: int
    explanation: str

    @classmethod
    def from_dict(cls, data: dict) -> 'StepMapping':
        return cls(
            ground_truth_step=data['ground_truth_step'],
            response_step=data['response_step'],
            confidence=data['confidence'],
            explanation=data['explanation']
        )

@dataclass
class ActivityComparison:
    activity_name: str
    step_mappings: List[StepMapping]
    unmatched_ground_truth_steps: List[str]
    unmatched_response_steps: List[str]
    missing_steps_explanation: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ActivityComparison':
        return cls(
            activity_name=data['activity_name'],
            step_mappings=[StepMapping.from_dict(sm) for sm in data['step_mappings']],
            unmatched_ground_truth_steps=data['unmatched_ground_truth_steps'],
            unmatched_response_steps=data['unmatched_response_steps'],
            missing_steps_explanation=data.get('missing_steps_explanation')
        )

@dataclass
class ActivityBreakdownComparison:
    comparisons: List[ActivityComparison]

    @classmethod
    def from_dict(cls, data: dict) -> 'ActivityBreakdownComparison':
        if isinstance(data, list):
            return cls(comparisons=[ActivityComparison.from_dict(ac) for ac in data])
        else:
            return cls(comparisons=[ActivityComparison.from_dict(data)])
           
        
def compare_activity_breakdown(gpt_breakdown: ProcessModel, ground_truth: ProcessModel) -> ActivityBreakdownComparison:
    comparator = ActivityBreakdownComparatorGPT()
    
    activity_comparison_dicts = []
    
    for gpt_activity, gt_activity in zip(gpt_breakdown.activities, ground_truth.activities):
        if gpt_activity.activity_name != gt_activity.activity_name:
            raise ValueError(f"Activity mismatch: {gpt_activity.activity_name} vs {gt_activity.activity_name}")
        
        activity_comparison_dict = comparator.compare_activity_breakdown(activity_ground_truth=gt_activity.to_dict(), activity_generation=gpt_activity.to_dict())
        
        activity_comparison = ActivityComparison.from_dict(activity_comparison_dict)
        
        activity_comparison_dicts.append(activity_comparison)
    
    return ActivityBreakdownComparison.from_dict(activity_comparison_dicts)
