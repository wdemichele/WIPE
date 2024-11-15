from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from .substep import SubStep

@dataclass
class UnmatchedStep:
    step: SubStep
    reason: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'UnmatchedStep':
        return UnmatchedStep(
            step=SubStep.from_dict({'step_number':data['step_number'], "description":data['description']}),
            reason=data['reason']
        )

    def to_dict(self) -> Dict[str, Any]:
        unmatched_dict = self.step.to_dict()
        unmatched_dict['reason'] = self.reason
        return unmatched_dict

@dataclass
class StepMapping:
    ground_truth_steps: List[SubStep]
    response_steps: List[SubStep]
    match_type: str
    confidence: int
    explanation: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'StepMapping':
        ground_truth_steps = [SubStep.from_dict(step) for step in data['ground_truth_steps']]
        response_steps = [SubStep.from_dict(step) for step in data['response_steps']]
        return StepMapping(
            ground_truth_steps=ground_truth_steps,
            response_steps=response_steps,
            match_type=data['match_type'],
            confidence=data['confidence'],
            explanation=data['explanation']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'ground_truth_steps': [step.to_dict() for step in self.ground_truth_steps],
            'response_steps': [step.to_dict() for step in self.response_steps],
            'match_type': self.match_type,
            'confidence': self.confidence,
            'explanation': self.explanation
        }

@dataclass
class ActivityBreakdownComparison:
    activity_name: str
    step_mappings: List[StepMapping]
    unmatched_ground_truth_steps: List[SubStep] = field(default_factory=list)
    unmatched_response_steps: List[SubStep] = field(default_factory=list)
    overall_similarity_score: float = 0.0
    missing_steps_explanation: str = ""

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ActivityBreakdownComparison':
        step_mappings = [StepMapping.from_dict(mapping) for mapping in data['step_mappings']]
        unmatched_ground_truth_steps = [UnmatchedStep.from_dict(step) for step in data.get('unmatched_ground_truth_steps', [])]
        unmatched_response_steps = [UnmatchedStep.from_dict(step) for step in data.get('unmatched_response_steps', [])]
        return ActivityBreakdownComparison(
            activity_name=data['activity_name'],
            step_mappings=step_mappings,
            unmatched_ground_truth_steps=unmatched_ground_truth_steps,
            unmatched_response_steps=unmatched_response_steps,
            overall_similarity_score=data['overall_similarity_score'],
            missing_steps_explanation=data['missing_steps_explanation']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'activity_name': self.activity_name,
            'step_mappings': [mapping.to_dict() for mapping in self.step_mappings],
            'unmatched_ground_truth_steps': [step.to_dict() for step in self.unmatched_ground_truth_steps],
            'unmatched_response_steps': [step.to_dict() for step in self.unmatched_response_steps],
            'overall_similarity_score': self.overall_similarity_score,
            'missing_steps_explanation': self.missing_steps_explanation
        }