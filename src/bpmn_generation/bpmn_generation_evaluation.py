from src.bpmn_generation import BPMNGenerationEvaluatorGPT
from src.bpmn_generation import MermaidImageGenerator
from src.bpmn_generation import BPMNGenerationGPT
from src.bpmn_generation.mermaid_syntax_correction_gpt import MermaidSyntaxCorrectionGPT

import os
ROOT_DIR = r"C:\Projects\Research\SWEEP\SWEEP"
class BPMNGenerationEvaluation:
    
    def __init__(self) -> None:
        self.evaluator = BPMNGenerationEvaluatorGPT()
        self.flow_image_generator = MermaidImageGenerator(mmdc_path=r"C:\Users\wmichele\AppData\Roaming\npm\mmdc.cmd")
        self.corrector = MermaidSyntaxCorrectionGPT()
    def generate_BPMN(self, sector: str, activity: str, train=True):
        folder_path = os.path.join(ROOT_DIR, f"data\\{'train' if train else 'test'}\\{sector}\\{activity}")
        image_name = f"{activity}_diagram.png"
        original_image_path = os.path.join(folder_path, image_name)
        
        bpmn_generator = BPMNGenerationGPT()
        mermaid_code = bpmn_generator.generate_bpmn(original_image_path)
        
        if mermaid_code:
            print(mermaid_code)
        else:
            print("Failed to generate BPMN notation.")
        
        # get the diagram name from the image path
        diagram_name = f"{activity}_diagram_generated.png"
        result_path = os.path.join(ROOT_DIR, f"test\\results\\bpmn_generation\\{'train' if train else 'test'}\\{sector}\\{activity}")

        if not os.path.exists(result_path):
            os.makedirs(result_path)
        
        generated_image_path = os.path.join(result_path, diagram_name)
        
        save_BPMN_success = self.save_BPMN_as_image(mermaid_code, generated_image_path)
        
        if not save_BPMN_success:
            print("Attempting to correct mermaid code...")
            mermaid_code = self.corrector.correct_mermaid_code(mermaid_code)
            save_BPMN_success = self.save_BPMN_as_image(mermaid_code, generated_image_path)
        
        equivalence, revisions = self.compare_BPMN_image_generation(original_image_path, generated_image_path)
        
        if not equivalence:
            final_equivalence, final_mermaid_code, final_revisions, num_iterations = self.revise_and_evaluate_bpmn(bpmn_generator, original_image_path, mermaid_code, revisions, result_path, image_name, iteration=0)
        else:
            final_equivalence = equivalence
            final_mermaid_code = mermaid_code
            final_revisions = revisions
            num_iterations = 1
        
        return final_equivalence, final_mermaid_code, final_revisions, num_iterations
        
    def save_BPMN_as_image(self, mermaid_code, generated_image_path):

        success = self.flow_image_generator.generate_image(mermaid_code, generated_image_path)
        
        return success
    
    def compare_BPMN_image_generation(self, original_image_path, generated_image_path):

        equivalance, revisions = self.evaluator.evaluate_bpmn(original_image_path, generated_image_path)

        if revisions:
            print("Evaluation Result:")
            print(f"equivalance: {equivalance}")
            
            print(revisions)
        else:
            print("Failed to evaluate BPMN diagrams.")
            
        return equivalance, revisions
    
    def revise_and_evaluate_bpmn(self, bpmn_generator: BPMNGenerationGPT, original_image_path, current_mermaid_code, revisions, result_path, image_name, iteration=0, max_iterations=5):
        """
        Recursively revise and evaluate BPMN diagrams.
        
        :param original_image_path: Path to the original image
        :param current_mermaid_code: Current Mermaid code to revise
        :param result_path: Path to the folder for saving generated images
        :param image_name: Name of the image file
        :param iteration: Current iteration count
        :param max_iterations: Maximum number of iterations allowed
        :return: Tuple of (final_equivalence, final_mermaid_code, final_revisions)
        """
        if iteration >= max_iterations:
            print(f"Reached maximum iterations ({max_iterations}). Stopping revision process.")
            return False, current_mermaid_code, "Max iterations reached. Further manual review may be needed.", iteration + 1

        # If not equivalent, revise the BPMN
        updated_mermaid_code = bpmn_generator.revise_bpmn(revisions)

        if updated_mermaid_code:
            print(f"\nUpdated Mermaid Code (Iteration {iteration + 1}):")
            print(updated_mermaid_code)
        else:
            print(f"Failed to generate BPMN notation in iteration {iteration + 1}.")
            return False, current_mermaid_code, "Failed to generate updated BPMN notation", iteration+1
        
        # Generate image from current Mermaid code
        revised_diagram_name = f"{image_name.split('.')[0]}_generated_revised_{iteration}.png"
        generated_revised_image_path = os.path.join(result_path, revised_diagram_name)
        success = self.flow_image_generator.generate_image(updated_mermaid_code, generated_revised_image_path)

        if not success:
            print(f"Failed to generate image for iteration {iteration}.")
            return False, current_mermaid_code, "Failed to generate image", iteration+1

        # Evaluate the revised BPMN
        equivalence, revisions = self.evaluator.evaluate_bpmn(original_image_path, generated_revised_image_path)

        print(f"\nIteration {iteration + 1} Evaluation Result:")
        print(f"Equivalence: {equivalence}")
        print(revisions)

        if equivalence:
            return True, updated_mermaid_code, revisions, iteration+1

        # Recursive call
        return self.revise_and_evaluate_bpmn(bpmn_generator,
            original_image_path, updated_mermaid_code, revisions,
            result_path, image_name, iteration + 1, max_iterations
        )