from dataclasses import dataclass, field
from typing import List, Optional
import json
from src.common.models.enum.value_category import ValueCategory
from .substep import SubStep
from .activity import Activity
from .process_model import ProcessModel

@dataclass
class ValueAddingAnalysis(ProcessModel):
    
    def classify(self, classification: str, activity: str, step: str, justification: str):
        activity_obj = self.get_activity(activity)
        if not activity_obj:
            print(f"Warning: Activity '{activity}' not found")
            return
        
        substep = activity_obj.get_substep(step)
        if not substep:
            print(f"Warning: Substep '{step}' not found in activity '{activity}'")
            return
        
        substep.classify(ValueCategory(classification), justification)
    
    def __str__(self):
        response = f'Value Adding Analysis: {self.name}'
        for activity in self.activities:
            response += f'\nActivity: {activity.activity_name}' 
            for substep in activity.substeps:
                response += f'\nStep {substep.step_number}: {substep.description}\nClassification: {substep.classification}\nReasoning: {substep.reasoning}\n'
                
        return response

    def to_dict(self) -> List[dict]:
        return [activity.to_dict(with_classification=True) for activity in self.activities]

    def classify_substeps(self, gpt_response: str):
        """
        Process the GPT response and update the ActivityBreakdown instance.
        """
        lines = gpt_response.strip().split('\n')
        for line in lines:
            if line.startswith('classify('):
                # Extract the arguments from the classify function call
                args = line.split('(', 1)[1].rsplit(')', 1)[0].split(',', 3)
                if len(args) != 4:
                    print(f"Warning: Invalid classify function call: {line}")
                    continue
                
                classification = args[0].strip().strip('"')
                activity = args[1].strip().strip('"')
                step = args[2].strip().strip('"')
                justification = args[3].strip().strip('"')
                
                # Call the classify method to update the ActivityBreakdown
                self.classify(classification, activity, step, justification)