from dataclasses import dataclass, field
from typing import List, Optional
from .substep import SubStep

@dataclass
class Activity:
    activity_name: str
    substeps: List[SubStep] = field(default_factory=list)
    
    def to_dict(self, with_classification=False) -> dict:
        return {
            'activity_name': self.activity_name,
            'substeps': [substep.to_dict(with_classification=with_classification) for substep in self.substeps]
        }        
    
    def get_substep(self, description: str) -> Optional[SubStep]:
        return next((step for step in self.substeps if step.description == description), None)