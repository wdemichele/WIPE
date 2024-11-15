from typing import List
from dataclasses import dataclass, field
from src.process.substep import SubStep


@dataclass
class Activity:
    activity_name: str
    substeps: List[SubStep] = None