from dataclasses import dataclass, field
from typing import List, Optional
import json
from src.common.models.enum.value_category import ValueCategory
from .substep import SubStep
from .activity import Activity
from .process_model import ProcessModel

@dataclass
class ActivityBreakdown(ProcessModel):
    
    def __str__(self):
        response = f'Activity Breakdown: {self.name}'
        for activity in self.activities:
            response += f'\nActivity: {activity.activity_name}' 
            for substep in activity.substeps:
                response += f'\nStep {substep.step_number}: {substep.description}\n'
                
        return response
                
    def to_dict(self) -> List[dict]:
        return [activity.to_dict(with_classification=False) for activity in self.activities]

