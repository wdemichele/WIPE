from typing import List, Dict, Optional
from .activity import Activity
from dataclasses import dataclass, field


class Process:
    def __init__(self, name: str):
        self.name = name
        self.activities: List[Activity] = []

    def add_activity(self, activity: Activity):
        self.activities.append(activity)
        
        
from typing import List
from .substep import SubStep


@dataclass
class Activity:
    activity_name: str
    substeps: List[SubStep] = None
    
from dataclasses import dataclass
from src.common.models.enum.value_category import ValueCategory

@dataclass
class SubStep:
    step_number: int
    description: Optional[str] = None
    value_category: Optional[ValueCategory] = None
    reasoning: Optional[str] = None

    def classify(self, category: ValueCategory):
        self.value_category = category
