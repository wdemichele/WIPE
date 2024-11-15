from dataclasses import dataclass, field
from typing import List, Optional
import json
from src.common.models.enum.value_category import ValueCategory
from .substep import SubStep
from .activity import Activity

@dataclass
class ProcessModel:
    name: str
    activities: List[Activity] = field(default_factory=list)
    
    def add_activity(self, activity: Activity):
        self.activities.append(activity)
        
    def get_activity(self, activity_name: str) -> Optional[Activity]:
        return next((activity for activity in self.activities if activity.activity_name == activity_name), None)
        
    @classmethod
    def from_dict(cls, name: str, data: List[dict]) -> 'ProcessModel':
        breakdown = cls(name)
        
        for activity_data in data:
            activity = Activity(activity_name=activity_data['activity_name'])
            for substep_data in activity_data['substeps']:
                substep = SubStep(
                    step_number=substep_data['step_number'],
                    description=substep_data['description'],
                    classification=ValueCategory(substep_data['classification']).value if substep_data.get('classification', None) else None,
                    reasoning=substep_data.get('reasoning', None)
                )
                activity.substeps.append(substep)
            breakdown.activities.append(activity)
            
        return breakdown
    
    @classmethod
    def from_json(cls, file_path: str) -> 'ProcessModel':
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        name = file_path.split('\\')[-2]
        
        breakdown = cls.from_dict(name, data)
        
        return breakdown
