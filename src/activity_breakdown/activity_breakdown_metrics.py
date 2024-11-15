from dataclasses import dataclass
from typing import List, Dict
from statistics import mean, median
from .activity_breakdown_comparison import ActivityBreakdownComparison

@dataclass
class ActivityBreakdownMetrics:
    total_activities: int
    total_ground_truth_steps: int
    total_response_steps: int
    total_matched_steps: int
    total_unmatched_ground_truth_steps: int
    total_unmatched_response_steps: int
    average_confidence_score: float
    median_confidence_score: float
    perfect_match_count: int
    perfect_match_percentage: float
    activity_coverage_percentage: float
    step_recall: float
    step_precision: float
    step_f1_score: float
    average_steps_per_activity: Dict[str, float]  # 'ground_truth' and 'response'
    confidence_distribution: Dict[str, int]  # Binned confidence scores
    
    def to_dict(self) -> dict:
        return {
            'total_activities': self.total_activities,
            'total_ground_truth_steps': self.total_ground_truth_steps,
            'total_response_steps': self.total_response_steps,
            'total_matched_steps': self.total_matched_steps,
            'total_unmatched_ground_truth_steps': self.total_unmatched_ground_truth_steps,
            'total_unmatched_response_steps': self.total_unmatched_response_steps,
            'average_confidence_score': self.average_confidence_score,
            'median_confidence_score': self.median_confidence_score,
            'perfect_match_count': self.perfect_match_count,
            'perfect_match_percentage': self.perfect_match_percentage,
            'activity_coverage_percentage': self.activity_coverage_percentage,
            'step_recall': self.step_recall,
            'step_precision': self.step_precision,
            'step_f1_score': self.step_f1_score,
            'average_steps_per_activity': self.average_steps_per_activity,
            'confidence_distribution': self.confidence_distribution
        }

def generate_activity_breakdown_metrics(ab_comparison: ActivityBreakdownComparison) -> 'ActivityBreakdownMetrics':
    total_activities = len(ab_comparison.comparisons)
    total_ground_truth_steps = sum(len(ac.step_mappings) + len(ac.unmatched_ground_truth_steps) for ac in ab_comparison.comparisons)
    total_response_steps = sum(len(ac.step_mappings) + len(ac.unmatched_response_steps) for ac in ab_comparison.comparisons)
    total_matched_steps = sum(len(ac.step_mappings) for ac in ab_comparison.comparisons)
    total_unmatched_ground_truth_steps = sum(len(ac.unmatched_ground_truth_steps) for ac in ab_comparison.comparisons)
    total_unmatched_response_steps = sum(len(ac.unmatched_response_steps) for ac in ab_comparison.comparisons)

    confidence_scores = [sm.confidence for ac in ab_comparison.comparisons for sm in ac.step_mappings]
    average_confidence_score = mean(confidence_scores) if confidence_scores else 0
    median_confidence_score = median(confidence_scores) if confidence_scores else 0

    perfect_match_count = sum(1 for ac in ab_comparison.comparisons if not ac.unmatched_ground_truth_steps and not ac.unmatched_response_steps)
    perfect_match_percentage = (perfect_match_count / total_activities) * 100 if total_activities > 0 else 0

    activity_coverage_percentage = (len([ac for ac in ab_comparison.comparisons if ac.step_mappings]) / total_activities) * 100 if total_activities > 0 else 0

    step_recall = total_matched_steps / total_ground_truth_steps if total_ground_truth_steps > 0 else 0
    step_precision = total_matched_steps / total_response_steps if total_response_steps > 0 else 0
    step_f1_score = 2 * (step_precision * step_recall) / (step_precision + step_recall) if (step_precision + step_recall) > 0 else 0

    average_steps_per_activity = {
        'ground_truth': total_ground_truth_steps / total_activities if total_activities > 0 else 0,
        'response': total_response_steps / total_activities if total_activities > 0 else 0
    }

    confidence_distribution = {
        '0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0
    }
    for score in confidence_scores:
        if score <= 20: confidence_distribution['0-20'] += 1
        elif score <= 40: confidence_distribution['21-40'] += 1
        elif score <= 60: confidence_distribution['41-60'] += 1
        elif score <= 80: confidence_distribution['61-80'] += 1
        else: confidence_distribution['81-100'] += 1

    return ActivityBreakdownMetrics(
        total_activities=total_activities,
        total_ground_truth_steps=total_ground_truth_steps,
        total_response_steps=total_response_steps,
        total_matched_steps=total_matched_steps,
        total_unmatched_ground_truth_steps=total_unmatched_ground_truth_steps,
        total_unmatched_response_steps=total_unmatched_response_steps,
        average_confidence_score=average_confidence_score,
        median_confidence_score=median_confidence_score,
        perfect_match_count=perfect_match_count,
        perfect_match_percentage=perfect_match_percentage,
        activity_coverage_percentage=activity_coverage_percentage,
        step_recall=step_recall,
        step_precision=step_precision,
        step_f1_score=step_f1_score,
        average_steps_per_activity=average_steps_per_activity,
        confidence_distribution=confidence_distribution
    )