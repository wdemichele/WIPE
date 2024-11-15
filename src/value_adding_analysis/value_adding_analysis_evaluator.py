import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.metrics import cohen_kappa_score
from scipy.stats import chi2_contingency

class ValueAddingAnalysisEvaluator:
    def __init__(self, analysis1, analysis2, analysis1_name='Analysis 1', analysis2_name='Analysis 2'):
        """
        Initialize the evaluator with two value-adding analyses.

        :param analysis1: List of activities for the first analysis.
        :param analysis2: List of activities for the second analysis.
        """
        self.analysis1 = analysis1
        self.analysis2 = analysis2
        self.analysis1_name = analysis1_name
        self.analysis2_name = analysis2_name

    def compute_metrics(self):
        """
        Compute metrics for comparison between the two analyses.
        """
        # Initialize lists to store substeps from both analyses
        self.analysis1_substeps = []
        self.analysis2_substeps = []

        # Process analysis1
        for activity in self.analysis1:
            activity_name = activity['activity_name']
            for substep in activity['substeps']:
                step = {
                    'activity_name': activity_name,
                    'step_number': substep['step_number'],
                    'classification': substep['classification']
                }
                self.analysis1_substeps.append(step)

        # Process analysis2
        for activity in self.analysis2:
            activity_name = activity['activity_name']
            for substep in activity['substeps']:
                step = {
                    'activity_name': activity_name,
                    'step_number': substep['step_number'],
                    'classification': substep['classification']
                }
                self.analysis2_substeps.append(step)

        # Compute classification counts for both analyses
        self.counts1 = {'VA': 0, 'BVA': 0, 'NVA': 0}
        self.counts2 = {'VA': 0, 'BVA': 0, 'NVA': 0}

        for step in self.analysis1_substeps:
            classification = step['classification']
            self.counts1[classification] += 1

        for step in self.analysis2_substeps:
            classification = step['classification']
            self.counts2[classification] += 1

        # Compute total steps and percentages
        self.total_steps1 = len(self.analysis1_substeps)
        self.total_steps2 = len(self.analysis2_substeps)

        self.percentages1 = {k: v / self.total_steps1 * 100 for k, v in self.counts1.items()}
        self.percentages2 = {k: v / self.total_steps2 * 100 for k, v in self.counts2.items()}

        # Identify classification changes between analyses
        self.classification_changes = []
        for step1, step2 in zip(self.analysis1_substeps, self.analysis2_substeps):
            if (step1['activity_name'] == step2['activity_name'] and 
                step1['step_number'] == step2['step_number']):
                if step1['classification'] != step2['classification']:
                    change = {
                        'activity_name': step1['activity_name'],
                        'step_number': step1['step_number'],
                        'classification1': step1['classification'],
                        'classification2': step2['classification']
                    }
                    self.classification_changes.append(change)
            else:
                # Handle mismatches in substeps if necessary
                pass  # Assuming substeps match for this implementation

        # Build confusion matrix between classifications
        self.confusion_matrix = defaultdict(lambda: defaultdict(int))
        for step1, step2 in zip(self.analysis1_substeps, self.analysis2_substeps):
            c1 = step1['classification']
            c2 = step2['classification']
            self.confusion_matrix[c1][c2] += 1

        # Compute Cohen's kappa for inter-rater reliability
        classifications1 = [step['classification'] for step in self.analysis1_substeps]
        classifications2 = [step['classification'] for step in self.analysis2_substeps]
        self.kappa = cohen_kappa_score(classifications1, classifications2, labels=['VA', 'BVA', 'NVA'])

        # Compute Fleiss' kappa
        self.fleiss_kappa = self.compute_fleiss_kappa()

        # Perform chi-squared test to compare distributions
        obs_counts1 = [self.counts1['VA'], self.counts1['BVA'], self.counts1['NVA']]
        obs_counts2 = [self.counts2['VA'], self.counts2['BVA'], self.counts2['NVA']]
        contingency_table = [obs_counts1, obs_counts2]

        # Check for zero counts
        if any(count == 0 for row in contingency_table for count in row):
            self.chi2 = None
            self.p_value = None
            print("Warning: Chi-square test not performed due to zero counts in the contingency table.")
        else:
            chi2, p, dof, expected = chi2_contingency(contingency_table)
            self.chi2 = chi2
            self.p_value = p

    def compute_fleiss_kappa(self):
        """
        Compute Fleiss' Kappa for inter-rater reliability.
        """
        n_items = len(self.analysis1_substeps)
        n_raters = 2  # We have two analyses
        n_categories = 3  # VA, BVA, NVA

        # Create a matrix where each row represents an item and each column represents a category
        ratings = np.zeros((n_items, n_categories))
        categories = {'VA': 0, 'BVA': 1, 'NVA': 2}

        for i in range(n_items):
            ratings[i, categories[self.analysis1_substeps[i]['classification']]] += 1
            ratings[i, categories[self.analysis2_substeps[i]['classification']]] += 1

        # Calculate P_i (proportion of agreement for each item)
        P_i = (np.sum(ratings ** 2, axis=1) - n_raters) / (n_raters * (n_raters - 1))
        P_bar = np.mean(P_i)

        # Calculate P_e (proportion of agreement expected by chance)
        P_e = np.sum((np.sum(ratings, axis=0) / (n_items * n_raters)) ** 2)

        # Calculate Fleiss' Kappa
        kappa = (P_bar - P_e) / (1 - P_e)

        return kappa

    def print_metrics(self):
        """
        Print the computed metrics for analysis.
        """
        print(f"{self.analysis1_name} Classification Counts:")
        for k, v in self.counts1.items():
            print(f"{k}: {v} ({self.percentages1[k]:.2f}%)")
        print(f"\n{self.analysis2_name} Classification Counts:")
        for k, v in self.counts2.items():
            print(f"{k}: {v} ({self.percentages2[k]:.2f}%)")
        print(f"\nTotal number of steps in {self.analysis1_name}:", self.total_steps1)
        print(f"Total number of steps in {self.analysis2_name}:", self.total_steps2)
        print("\nNumber of classification changes between analyses:", len(self.classification_changes))
        print("\nCohen's Kappa:", self.kappa)
        print("Fleiss' Kappa:", self.fleiss_kappa)
        print("Chi-squared test statistic:", self.chi2)
        print("p-value:", self.p_value)

    def display_graphs(self):
        """
        Display graphs for the evaluated comparisons.
        """
        # Bar chart of classification counts
        classifications = ['VA', 'BVA', 'NVA']
        counts1 = [self.counts1[c] for c in classifications]
        counts2 = [self.counts2[c] for c in classifications]

        x = range(len(classifications))
        width = 0.35

        fig, ax = plt.subplots()
        ax.bar([i - width/2 for i in x], counts1, width, label=f'{self.analysis1_name}')
        ax.bar([i + width/2 for i in x], counts2, width, label=f'{self.analysis2_name}')

        ax.set_ylabel('Counts')
        ax.set_title('Classification Counts')
        ax.set_xticks(x)
        ax.set_xticklabels(classifications)
        ax.legend()

        plt.show()

        # Define the desired order
        order = ["VA", "BVA", "NVA"]

        # Confusion matrix heatmap
        confusion_df = pd.DataFrame(self.confusion_matrix).fillna(0).astype(int)

        # Reindex the DataFrame to ensure the desired order
        confusion_df = confusion_df.reindex(index=order, columns=order, fill_value=0)

        plt.figure(figsize=(8, 6))
        sns.heatmap(confusion_df, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.xlabel(f'{self.analysis1_name} Classification')
        plt.ylabel(f'{self.analysis2_name} Classification')
        plt.show()
