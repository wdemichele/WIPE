from typing import List, Dict, Optional
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
