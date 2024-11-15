from dataclasses import dataclass
from typing import Optional
from src.common.models.enum.value_category import ValueCategory
from typing import Dict, Any

@dataclass
class SubStep:
    step_number: int
    description: str
    classification: Optional[ValueCategory] = None
    reasoning: Optional[str] = None
    
    def to_dict(self, with_classification=False) -> dict:
        substep_dict = {
            'step_number': self.step_number,
            'description': self.description
        }
        
        if with_classification:
            substep_dict['classification'] = self.classification
            substep_dict['reasoning'] = self.reasoning
        
        return substep_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubStep':
        return cls(**data)
    
    def classify(self, category: ValueCategory, reasoning: str):
        self.classification = category.value if isinstance(category, ValueCategory) else category
        self.reasoning = reasoning
