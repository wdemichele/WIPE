from src.bpmn_generation import BPMNGenerationGPT, MermaidImageGenerator, BPMNGenerationEvaluatorGPT
from src.common.util import ImageUtils

class BPMNGenerator:
    def __init__(self, verbose=False):

        bpmn_generator = BPMNGenerationGPT()
        image_generator = MermaidImageGenerator(mmdc_path=r"C:\Users\wmichele\AppData\Roaming\npm\mmdc.cmd")
        evaluator = BPMNGenerationEvaluatorGPT()

        self.bpmn_generator: BPMNGenerationGPT = bpmn_generator
        self.image_generator: MermaidImageGenerator = image_generator
        self.evaluator: BPMNGenerationEvaluatorGPT = evaluator
        self.verbose = verbose

    def log(self, message):
        """Print message if verbose mode is on."""
        if self.verbose:
            print(message)

    def generate_initial_bpmn(self, image_path):
        """Generate initial BPMN Mermaid code from an image."""
        mermaid_code = self.bpmn_generator.generate_bpmn(image_path)
        if mermaid_code:
            self.log("Initial Mermaid Code:")
            self.log(mermaid_code)
        else:
            self.log("Failed to generate initial BPMN notation.")
        return mermaid_code

    def generate_bpmn_image(self, mermaid_code, output_path):
        """Generate an image from BPMN Mermaid code."""
        success = self.image_generator.generate_image(mermaid_code, output_path)
        if not success:
            self.log(f"Failed to generate image at {output_path}")
        return success

    def evaluate_bpmn(self, original_image_path, generated_image_path):
        """Evaluate the generated BPMN against the original."""
        equivalence, revisions = self.evaluator.evaluate_bpmn(original_image_path, generated_image_path)
        self.log("Evaluation Result:")
        self.log(f"Equivalence: {equivalence}")
        self.log(revisions)
        return equivalence, revisions

    def revise_bpmn(self, revisions):
        """Revise the BPMN based on evaluation feedback."""
        return self.bpmn_generator.revise_bpmn(revisions)

    def generate_bpmn(self, original_image_path, output_image_path, max_iterations=3, plot=True):
        """Process BPMN generation, evaluation, and revision."""
        mermaid_code = self.generate_initial_bpmn(original_image_path)
        if not mermaid_code:
            return False, None, "Failed to generate initial BPMN", 1

        for iteration in range(max_iterations):
            self.log(f"\nIteration {iteration + 1}")
            success = self.generate_bpmn_image(mermaid_code, output_image_path)
            if not success:
                return False, mermaid_code, f"Failed to generate image in iteration {iteration + 1}", iteration + 1

            equivalence, revisions = self.evaluate_bpmn(original_image_path, output_image_path)
            if equivalence:
                if plot:
                    ImageUtils.plot_image_from_path(output_image_path, title="Generated BPMN")
                return True, mermaid_code, "BPMN is equivalent", iteration + 1

            mermaid_code = self.revise_bpmn(revisions)
            if not mermaid_code:
                return False, None, f"Failed to revise BPMN in iteration {iteration + 1}"

            self.log(f"Updated Mermaid Code:")
            self.log(mermaid_code)

        return False, mermaid_code, f"Max iterations of {max_iterations} reached without achieving equivalence"

# Usage example
if __name__ == "__main__":
    import os

    ROOT_DIR = r"C:\Projects\Research\SWEEP\SWEEP"

    sector = "banking"
    activity = "loan_risk_assessment"
    
    original_image_path = os.path.join(ROOT_DIR, f"data\\{sector}\\{activity}", f"{activity}_diagram.png")
    output_folder = os.path.join(ROOT_DIR, f"test\\results\\bpmn_generation\\{sector}\\{activity}")
    os.makedirs(output_folder, exist_ok=True)
    output_image_path = os.path.join(output_folder, f"{activity}_generated.png")
    

    bpmn_manager = BPMNGenerator(verbose=False)
    success, final_mermaid_code, message, iterations = bpmn_manager.generate_bpmn(original_image_path, output_image_path)

    print("\nFinal Result:", message)
    if success:
        print("Final Mermaid Code:")
        print(final_mermaid_code)
    elif final_mermaid_code:
        print("Last Mermaid Code:")
        print(final_mermaid_code)