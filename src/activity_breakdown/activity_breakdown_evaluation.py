import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict
from src.activity_breakdown import ActivityBreakdownComparatorGPT, ActivityBreakdownComparison

class ActivityBreakdownEvaluation:
    def __init__(self):
        self.comparator = ActivityBreakdownComparatorGPT()
        self.comparison_data = []

    def compare_activity_breakdowns(self, ground_truth_data: List[Dict], activity_breakdown: List[Dict]) -> List[ActivityBreakdownComparison]:
        self.comparison_data = []
        for i, (ground_truth, activity) in enumerate(zip(ground_truth_data, activity_breakdown)):
            print(f"Comparing activity {i+1}...")
            comparison_object = self.comparator.compare_activity_breakdown(ground_truth, activity)
            self.comparison_data.append(comparison_object)
        return self.comparison_data

    def get_comparison_data(self) -> List[ActivityBreakdownComparison]:
        return self.comparison_data

    @staticmethod
    def evaluate_comparisons(comparison_data, plot=True) -> Dict:
        # Initialize accumulators for metrics
        match_type_counts = Counter()
        confidence_scores = []
        match_type_confidences = defaultdict(list)
        ground_truth_steps_total = 0
        response_steps_total = 0
        ground_truth_steps_matched = 0
        response_steps_matched = 0
        sequence_alignment_scores = []
        overall_similarity_scores = []

        # Collect data for qualitative analysis
        examples_by_match_type = defaultdict(list)
        unmatched_ground_truth_steps = []
        unmatched_response_steps = []
        granularity_issues = []

        for activity in comparison_data:
            activity_name = activity['activity_name']
            step_mappings = activity['step_mappings']
            unmatched_gt_steps = activity.get('unmatched_ground_truth_steps', [])
            unmatched_resp_steps = activity.get('unmatched_response_steps', [])
            overall_similarity_score = activity.get('overall_similarity_score', 0)

            # Update overall similarity scores
            overall_similarity_scores.append(overall_similarity_score)

            # Update total steps
            num_ground_truth_steps = sum(len(mapping['ground_truth_steps']) for mapping in step_mappings) + len(unmatched_gt_steps)
            num_response_steps = sum(len(mapping['response_steps']) for mapping in step_mappings) + len(unmatched_resp_steps)
            ground_truth_steps_total += num_ground_truth_steps
            response_steps_total += num_response_steps

            # Update matched steps
            matched_gt_steps = sum(len(mapping['ground_truth_steps']) for mapping in step_mappings)
            matched_resp_steps = sum(len(mapping['response_steps']) for mapping in step_mappings)
            ground_truth_steps_matched += matched_gt_steps
            response_steps_matched += matched_resp_steps

            # Update match type counts and confidences
            for mapping in step_mappings:
                match_type = mapping['match_type']
                confidence = mapping['confidence']
                match_type_counts[match_type] += 1
                confidence_scores.append(confidence)
                match_type_confidences[match_type].append(confidence)

                # Collect examples for qualitative analysis
                examples_by_match_type[match_type].append({
                    'activity_name': activity_name,
                    'ground_truth_steps': mapping['ground_truth_steps'],
                    'response_steps': mapping['response_steps'],
                    'confidence': confidence,
                    'explanation': mapping['explanation']
                })

                # Check for granularity issues
                if len(mapping['ground_truth_steps']) != len(mapping['response_steps']):
                    granularity_issues.append({
                        'activity_name': activity_name,
                        'mapping': mapping
                    })

            # Collect unmatched steps for qualitative analysis
            for step in unmatched_gt_steps:
                unmatched_ground_truth_steps.append({
                    'activity_name': activity_name,
                    'step': step
                })

            for step in unmatched_resp_steps:
                unmatched_response_steps.append({
                    'activity_name': activity_name,
                    'step': step
                })

            # Sequence Alignment (Simple Measure)
            gt_step_numbers = [gt_step['step_number'] for mapping in step_mappings for gt_step in mapping['ground_truth_steps']]
            resp_step_numbers = [resp_step['step_number'] for mapping in step_mappings for resp_step in mapping['response_steps']]

            # Simple ratio of steps in correct order
            sequence_score = ActivityBreakdownEvaluation.compute_sequence_alignment(gt_step_numbers, resp_step_numbers)
            sequence_alignment_scores.append(sequence_score)

        # Compute quantitative metrics
        metrics = {}

        # Match Type Distribution
        total_matches = sum(match_type_counts.values())
        metrics['match_type_distribution'] = {k: (v, v / total_matches * 100) for k, v in match_type_counts.items()}

        # Average Confidence Scores
        metrics['average_confidence'] = np.mean(confidence_scores)
        metrics['average_confidence_by_match_type'] = {k: np.mean(v) for k, v in match_type_confidences.items()}

        # Step Matching Rates
        metrics['ground_truth_coverage'] = ground_truth_steps_matched / ground_truth_steps_total * 100 if ground_truth_steps_total else 0
        metrics['response_coverage'] = response_steps_matched / response_steps_total * 100 if response_steps_total else 0

        # Sequence Alignment
        metrics['average_sequence_alignment'] = np.mean(sequence_alignment_scores)

        # Overall Similarity Score
        metrics['average_overall_similarity_score'] = np.mean(overall_similarity_scores)

        # Generate reports
        ActivityBreakdownEvaluation.generate_reports(metrics, examples_by_match_type, unmatched_ground_truth_steps, unmatched_response_steps, granularity_issues, plot)
        
        return metrics

    @staticmethod
    def compute_sequence_alignment(gt_steps, resp_steps):
        # Simple sequence alignment score
        # Counts the number of steps in the correct relative order
        matches = 0
        for i in range(min(len(gt_steps), len(resp_steps))):
            if gt_steps[i] == resp_steps[i]:
                matches += 1
        return matches / max(len(gt_steps), len(resp_steps)) * 100 if max(len(gt_steps), len(resp_steps)) else 0

    @staticmethod
    def generate_reports(metrics, examples_by_match_type, unmatched_gt_steps, unmatched_resp_steps, granularity_issues, plot):
        # Print quantitative metrics
        print("Quantitative Metrics:")
        print("=====================")
        print(f"Total Activities Evaluated: {len(metrics['match_type_distribution'])}")
        print(f"Average Overall Similarity Score: {metrics['average_overall_similarity_score']:.2f}%")
        print(f"Average Confidence Score: {metrics['average_confidence']:.2f}%")
        print(f"Average Sequence Alignment Score: {metrics['average_sequence_alignment']:.2f}%")
        print(f"Ground Truth Steps Coverage: {metrics['ground_truth_coverage']:.2f}%")
        print(f"Response Steps Coverage: {metrics['response_coverage']:.2f}%\n")

        print("Match Type Distribution:")
        for match_type, (count, percentage) in metrics['match_type_distribution'].items():
            avg_confidence = metrics['average_confidence_by_match_type'][match_type]
            print(f"- {match_type}: {count} matches ({percentage:.2f}%), Average Confidence: {avg_confidence:.2f}%")
        print("\n")

        # Generate charts
        if plot:
            ActivityBreakdownEvaluation.plot_match_type_distribution(metrics['match_type_distribution'])
            ActivityBreakdownEvaluation.plot_confidence_by_match_type(metrics['average_confidence_by_match_type'])

        # Qualitative Analysis
        print("Qualitative Analysis:")
        print("=====================\n")

        print("Examples of Matched Steps by Match Type:\n")
        for match_type, examples in examples_by_match_type.items():
            print(f"Match Type: {match_type}")
            for example in examples[:3]:  # Limit to first 3 examples
                print(f"Activity: {example['activity_name']}")
                print("Ground Truth Steps:")
                for step in example['ground_truth_steps']:
                    print(f"  - [{step['step_number']}] {step['description']}")
                print("Response Steps:")
                for step in example['response_steps']:
                    print(f"  - [{step['step_number']}] {step['description']}")
                print(f"Confidence: {example['confidence']}%")
                print(f"Explanation: {example['explanation']}\n")
            print("\n")

        print("Analysis of Unmatched Ground Truth Steps:")
        for item in unmatched_gt_steps[:5]:  # Limit to first 5
            print(f"Activity: {item['activity_name']}, Step: [{item['step']['step_number']}] {item['step']['description']}")
            print(f"Reason: {item['step'].get('reason', 'No reason provided')}\n")

        print("Analysis of Unmatched Response Steps:")
        for item in unmatched_resp_steps[:5]:  # Limit to first 5
            print(f"Activity: {item['activity_name']}, Step: [{item['step']['step_number']}] {item['step']['description']}")
            print(f"Reason: {item['step'].get('reason', 'No reason provided')}\n")

        print("Granularity Issues Identified:")
        for issue in granularity_issues[:5]:  # Limit to first 5
            mapping = issue['mapping']
            print(f"Activity: {issue['activity_name']}")
            print("Ground Truth Steps:")
            for step in mapping['ground_truth_steps']:
                print(f"  - [{step['step_number']}] {step['description']}")
            print("Response Steps:")
            for step in mapping['response_steps']:
                print(f"  - [{step['step_number']}] {step['description']}")
            print(f"Explanation: {mapping['explanation']}\n")

    @staticmethod
    def plot_match_type_distribution(match_type_distribution):
        match_types = list(match_type_distribution.keys())
        percentages = [match_type_distribution[mt][1] for mt in match_types]

        plt.figure(figsize=(10, 6))
        # sns.set_style("whitegrid")
        # sns.set_palette("deep")
        
        ax = sns.barplot(x=match_types, y=percentages)
        
        plt.title('Match Type Distribution') #, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Match Type', fontsize=12, labelpad=10)
        plt.ylabel('Percentage (%)', fontsize=12, labelpad=10)
        
        # Add value labels on top of each bar
        for i, p in enumerate(ax.patches):
            ax.annotate(f'{percentages[i]:.1f}%', 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')

        # Improve x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        # Add a light grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()
        
    @staticmethod
    def plot_confidence_by_match_type(average_confidence_by_match_type):
        match_types = list(average_confidence_by_match_type.keys())
        confidences = [average_confidence_by_match_type[mt] for mt in match_types]

        plt.figure(figsize=(10, 6))
        # sns.set_style("whitegrid")
        # sns.set_palette("deep")
        
        ax = sns.barplot(x=match_types, y=confidences)
        
        plt.title('Average Confidence Score by Match Type') #, fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Match Type', fontsize=12, labelpad=10)
        plt.ylabel('Average Confidence (%)', fontsize=12, labelpad=10)
        
        # Add value labels on top of each bar
        for i, p in enumerate(ax.patches):
            ax.annotate(f'{confidences[i]:.1f}%', 
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha = 'center', va = 'center', 
                        xytext = (0, 9), 
                        textcoords = 'offset points')

        # Improve x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        # Add a light grid
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adjust layout and display
        plt.tight_layout()
        plt.show()