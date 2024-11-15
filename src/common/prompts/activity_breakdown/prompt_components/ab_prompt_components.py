from dataclasses import dataclass, field
from typing import Optional, Dict, Any

# Import statements for the component variations
from .role_description import ROLE_DESCRIPTIONS
from .output_format import OUTPUT_FORMATS
from .focus_shifts import FOCUS_SHIFTS
from .guidelines import GUIDELINES
from .task_descriptions import TASK_DESCRIPTIONS
from .example_output import EXAMPLE_OUTPUTS

# Dictionary of prompt components
PROMPT_COMPONENTS = {
    'role_description': ROLE_DESCRIPTIONS,
    'task_description': TASK_DESCRIPTIONS,
    'guidelines': GUIDELINES,
    'output_format': OUTPUT_FORMATS,
    'example_output': EXAMPLE_OUTPUTS,
    'focus_shift': FOCUS_SHIFTS,
}

@dataclass
class ABPromptComponents:
    role_description: Optional[str] = None
    task_description: Optional[str] = None
    classification_types: Optional[str] = None
    function_definition: Optional[str] = None
    parsing_instructions: Optional[str] = None
    output_format: Optional[str] = None
    example_output: Optional[str] = None
    additional_guidelines: Optional[str] = None
    _raw_input: Dict[str, Any] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        for key, value in self._raw_input.items():
            if key in PROMPT_COMPONENTS:
                if value in PROMPT_COMPONENTS[key]:
                    setattr(self, key, PROMPT_COMPONENTS[key][value])
                else:
                    raise ValueError(f"Invalid variation '{value}' for component '{key}'")
            else:
                raise ValueError(f"Invalid component '{key}'")

    @classmethod
    def from_dict(cls, input_dict: Dict[str, Any]):
        return cls(_raw_input=input_dict)