import numpy as np
from sklearn.metrics import cohen_kappa_score
from collections import defaultdict
from sklearn.metrics import confusion_matrix
from sklearn.metrics import matthews_corrcoef

class InterAnnotatorAgreement:
    def __init__(self):
        # Stores annotations with substep IDs as keys and annotator annotations as values
        self.annotations = {}  # {substep_id: {annotator_name: classification}}
        self.annotators = set()
        self.categories = set()

    def add_annotations(self, case_name, annotator_name, data):
        self.annotators.add(annotator_name)
        for activity in data:
            activity_name = activity['activity_name']
            for substep in activity['substeps']:
                step_number = substep['step_number']
                classification = substep['classification']
                self.categories.add(classification)
                substep_id = f"{case_name}::{activity_name}::{step_number}"
                if substep_id not in self.annotations:
                    self.annotations[substep_id] = {}
                self.annotations[substep_id][annotator_name] = classification

    def compute_pairwise_cohen_kappa(self):
        """
        Computes pairwise Cohen's Kappa for all pairs of annotators.

        Returns:
        - kappa_scores (dict): Dictionary with annotator pairs as keys and Kappa scores as values.
        """
        annotators = list(self.annotators)
        kappa_scores = {}
        for i in range(len(annotators)):
            for j in range(i + 1, len(annotators)):
                annotator_a = annotators[i]
                annotator_b = annotators[j]
                labels_a, labels_b = self._get_common_annotations(annotator_a, annotator_b)
                if labels_a:
                    kappa = cohen_kappa_score(labels_a, labels_b)
                    kappa_scores[(annotator_a, annotator_b)] = kappa
        return kappa_scores

    def compute_pairwise_percent_agreement(self):
        """
        Computes pairwise percent agreement for all pairs of annotators.

        Returns:
        - agreement_scores (dict): Dictionary with annotator pairs as keys and percent agreement as values.
        """
        annotators = list(self.annotators)
        agreement_scores = {}
        for i in range(len(annotators)):
            for j in range(i + 1, len(annotators)):
                annotator_a = annotators[i]
                annotator_b = annotators[j]
                labels_a, labels_b = self._get_common_annotations(annotator_a, annotator_b)
                if labels_a:
                    agreements = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
                    percent_agreement = agreements / len(labels_a)
                    agreement_scores[(annotator_a, annotator_b)] = percent_agreement
        return agreement_scores

    def _get_common_annotations(self, annotator_a, annotator_b):
        """
        Retrieves the annotations for items annotated by both annotators.

        Returns:
        - labels_a (list): Annotations from annotator_a.
        - labels_b (list): Annotations from annotator_b.
        """
        labels_a = []
        labels_b = []
        for substep_id, annotations in self.annotations.items():
            if annotator_a in annotations and annotator_b in annotations:
                labels_a.append(annotations[annotator_a])
                labels_b.append(annotations[annotator_b])
        return labels_a, labels_b

    def compute_krippendorff_alpha(self):
        """
        Computes Krippendorff's Alpha for nominal data.

        Returns:
        - alpha (float): Krippendorff's Alpha coefficient.
        """
        # Map categories and annotators to indices
        categories = list(self.categories)
        category_to_index = {category: idx for idx, category in enumerate(categories)}
        annotators = list(self.annotators)
        annotator_to_index = {annotator: idx for idx, annotator in enumerate(annotators)}

        # Initialize the data matrix with NaNs (items x annotators)
        data_matrix = np.full((len(self.annotations), len(annotators)), np.nan)

        # Populate the data matrix with annotations
        for i, (substep_id, annotator_annotations) in enumerate(self.annotations.items()):
            for annotator, annotation in annotator_annotations.items():
                j = annotator_to_index[annotator]
                data_matrix[i, j] = category_to_index[annotation]

        # Compute Krippendorff's Alpha
        alpha = self.krippendorffs_alpha(data_matrix)
        return alpha

    @staticmethod
    def krippendorffs_alpha(data_matrix):
        """
        Calculates Krippendorff's Alpha for nominal data.

        Parameters:
        - data_matrix (np.ndarray): Annotation matrix with shape (items x annotators).

        Returns:
        - alpha (float): Krippendorff's Alpha coefficient.
        """
        def nominal_metric(a, b):
            return 0 if a == b else 1

        # Collect all pairs of annotations for each item
        Do, n_o = 0, 0
        for ratings in data_matrix:
            valid_ratings = ratings[~np.isnan(ratings)]
            n = len(valid_ratings)
            if n > 1:
                # Number of pairs is n * (n - 1) / 2
                n_pairs = n * (n - 1) / 2
                disagreements = sum(nominal_metric(valid_ratings[i], valid_ratings[j])
                                    for i in range(n) for j in range(i + 1, n))
                Do += disagreements
                n_o += n_pairs

        Do = Do / n_o if n_o > 0 else 0

        # Calculate expected disagreement De
        valid_data = data_matrix[~np.isnan(data_matrix)]
        categories, counts = np.unique(valid_data, return_counts=True)
        total = counts.sum()
        probabilities = counts / total
        De = 1 - sum(p ** 2 for p in probabilities)

        # Compute Krippendorff's Alpha
        alpha = 1 - (Do / De) if De != 0 else 1.0
        return alpha

    def compute_precision_recall_f1(self, target_class='NVA'):
        """
        Computes precision, recall, and F1-score for the specified target class (e.g., 'NVA').

        Returns:
        - metrics (dict): Dictionary with annotator names as keys and their precision, recall, and F1-score as values.
        """
        metrics = {}
        for annotator in self.annotators:
            true_positives = 0
            false_positives = 0
            false_negatives = 0

            for substep_id, annotations in self.annotations.items():
                # Skip if the annotator did not annotate this item
                if annotator not in annotations:
                    continue

                annotator_label = annotations[annotator]
                # Get the majority label or compare against other annotators
                other_labels = [label for a, label in annotations.items() if a != annotator]

                # For binary classification, consider merging categories if needed
                # Merge VA and BVA into 'Other' category
                other_labels_simplified = ['Other' if label != target_class else label for label in other_labels]
                annotator_label_simplified = 'Other' if annotator_label != target_class else annotator_label

                # Count true positives, false positives, and false negatives
                if annotator_label_simplified == target_class:
                    if target_class in other_labels_simplified:
                        true_positives += 1
                    else:
                        false_positives += 1
                else:
                    if target_class in other_labels_simplified:
                        false_negatives += 1

            # Calculate precision, recall, and F1-score
            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            if precision + recall > 0:
                f1_score = 2 * (precision * recall) / (precision + recall)
            else:
                f1_score = 0

            metrics[annotator] = {
                'precision': precision,
                'recall': recall,
                'f1_score': f1_score
            }
        return metrics
    
    def compute_pairwise_confusion_matrices(self):
        """
        Computes confusion matrices for all pairs of annotators.

        Returns:
        - confusion_matrices (dict): Dictionary with annotator pairs as keys and confusion matrices as values.
        """
        annotators = list(self.annotators)
        confusion_matrices = {}
        categories = list(self.categories)
        for i in range(len(annotators)):
            for j in range(i + 1, len(annotators)):
                annotator_a = annotators[i]
                annotator_b = annotators[j]
                labels_a, labels_b = self._get_common_annotations(annotator_a, annotator_b)
                if labels_a:
                    cm = confusion_matrix(labels_a, labels_b, labels=categories)
                    confusion_matrices[(annotator_a, annotator_b)] = cm
        return confusion_matrices, categories
    
    def compute_pairwise_mcc(self):
        """
        Computes pairwise Matthews Correlation Coefficient (MCC) for all pairs of annotators after merging VA and BVA.

        Returns:
        - mcc_scores (dict): Dictionary with annotator pairs as keys and MCC scores as values.
        """
        annotators = list(self.annotators)
        mcc_scores = {}
        for i in range(len(annotators)):
            for j in range(i + 1, len(annotators)):
                annotator_a = annotators[i]
                annotator_b = annotators[j]
                labels_a, labels_b = self._get_common_annotations(annotator_a, annotator_b)
                if labels_a:
                    # Simplify labels by merging VA and BVA
                    labels_a_binary = ['NVA' if label == 'NVA' else 'VA_BVA' for label in labels_a]
                    labels_b_binary = ['NVA' if label == 'NVA' else 'VA_BVA' for label in labels_b]
                    mcc = matthews_corrcoef(labels_a_binary, labels_b_binary)
                    mcc_scores[(annotator_a, annotator_b)] = mcc
        return mcc_scores