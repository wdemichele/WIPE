import os
from src.common.models import BPMNModel, ProcessModel, ActivityBreakdown, ValueAddingAnalysis
from src.bpmn_generation import BPMNGenerator
from src.activity_breakdown import ActivityBreakdownGPT
from src.value_adding_analysis import ValueClassificationComponentsGPT, PromptComponents

def main(sector: str, activity: str, root_dir: str, verbose=True):
    # Folder setup
    process_model_image, output_image_path, _ = setup_folders(root_dir, sector, activity)
    
    # BPMN Generation
    print("Generating BPMN model...")
    bpmn_generation_response = generate_bpmn(process_model_image, output_image_path, verbose)
    
    # Activity Breakdown
    print("Performing activity breakdown...")
    model_activity_breakdown = perform_activity_breakdown(activity, bpmn_generation_response, verbose)
    
    # Value Adding Analysis
    print("Performing value adding analysis...")
    model_value_adding_analysis = perform_value_adding_analysis(model_activity_breakdown, verbose)
    
    return bpmn_generation_response, model_activity_breakdown, model_value_adding_analysis

def setup_folders(root_dir, sector, activity):
    """Set up the necessary folders for the analysis."""
    process_model_image = os.path.join(root_dir, f"data\\{sector}\\{activity}", f"{activity}_diagram.png")
    results_folder = os.path.join(root_dir, f"test\\results")
    
    folders = {
        'bpmn_generation': os.path.join(results_folder, f"bpmn_generation\\{sector}\\{activity}"),
        'activity_breakdown': os.path.join(results_folder, f"activity_breakdown\\{sector}\\{activity}"),
        'value_adding_analysis': os.path.join(results_folder, f"value_adding_analysis\\{sector}\\{activity}")
    }
    
    for folder in folders.values():
        os.makedirs(folder, exist_ok=True)
    
    output_image_path = os.path.join(folders['bpmn_generation'], f"{activity}_generated.png")
    
    return process_model_image, output_image_path, folders

def generate_bpmn(process_model_image, output_image_path, verbose=True):
    """Generate BPMN model."""
    bpmn_manager = BPMNGenerator(verbose=False)
    success, bpmn_generation_response, message, iterations = bpmn_manager.generate_bpmn(process_model_image, output_image_path)

    if verbose:
        print_bpmn_generation_results(success, message, iterations, bpmn_generation_response)
    
    return bpmn_generation_response

def perform_activity_breakdown(activity, bpmn_generation_response, verbose=True):
    """Perform activity breakdown."""
    bpmn_model = BPMNModel.from_str(activity, bpmn_generation_response)
    activity_decomposer = ActivityBreakdownGPT(prompt_components=None)
    activity_breakdown_response = activity_decomposer.bpmn_activity_breakdown(bpmn_model.model)
    model_activity_breakdown = ActivityBreakdown.from_dict(activity, activity_breakdown_response)
    
    if verbose:
        print_activity_breakdown_results(model_activity_breakdown)
    
    return model_activity_breakdown

def perform_value_adding_analysis(model_activity_breakdown: ActivityBreakdown, verbose=True):
    """Perform value adding analysis."""
    activity_breakdown_dict: ActivityBreakdown = model_activity_breakdown.to_dict()
    value_classifier = ValueClassificationComponentsGPT(prompt_components=PromptComponents.from_dict({
        "role_description": "neutral_analyst",
        "task_description": "standard",
        "classification_types": "basic",
        "function_definition": "basic",
        "parsing_instructions": "sequential",
        "output_format": "basic"
    }))
    
    model_value_adding_analysis: ValueAddingAnalysis = ValueAddingAnalysis.from_dict(activity_breakdown_dict.name, activity_breakdown_dict.to_dict())
    
    value_adding_analysis_response = value_classifier.value_classification_step_level(activity_breakdown_dict)
    model_value_adding_analysis.classify_substeps(value_adding_analysis_response)
    
    if verbose:
        print_value_adding_analysis_results(model_value_adding_analysis)
    
    return model_value_adding_analysis

def print_bpmn_generation_results(success, message, iterations, bpmn_generation_response):
    """Print BPMN generation results."""
    print("+"*50)
    print("\nFinal Result:", message)
    print(f"Total Iterations: {iterations}")
    if success:
        print("Final Mermaid Code:")
        print(bpmn_generation_response)
    elif bpmn_generation_response:
        print("Last Mermaid Code:")
        print(bpmn_generation_response)
    print("+"*50)

def print_activity_breakdown_results(model_activity_breakdown):
    """Print activity breakdown results."""
    print("+"*50)
    print("\nActivity Breakdown:")
    print(model_activity_breakdown)
    print("+"*50)

def print_value_adding_analysis_results(model_activity_breakdown):
    """Print value adding analysis results."""
    print("+"*50)
    print("\nValue Adding Analysis:")
    print(model_activity_breakdown)
    print("+"*50)

if __name__ == "__main__":
    # Example usage
    sector = "example_sector"
    activity = "example_activity"
    root_dir = "path/to/root/directory"
    main(sector, activity, root_dir, verbose=True)