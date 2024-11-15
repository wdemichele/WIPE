from dataclasses import dataclass, field
from typing import Optional, Dict, Any

# Import statements for the component variations
from .role_description import ROLE_DESCRIPTIONS
from .task_description import TASK_DESCRIPTIONS
from .classification_types import CLASSIFICATION_TYPES
from .function_definition import FUNCTION_DEFINITIONS
from .parsing_instructions import PARSING_INSTRUCTIONS
from .output_format import OUTPUT_FORMATS
from .example_output import EXAMPLE_OUTPUTS
from .additional_guidelines import ADDITIONAL_GUIDELINES

# Dictionary of prompt components
PROMPT_COMPONENTS = {
    "role_description": ROLE_DESCRIPTIONS,
    "task_description": TASK_DESCRIPTIONS,
    "classification_types": CLASSIFICATION_TYPES,
    "function_definition": FUNCTION_DEFINITIONS,
    "parsing_instructions": PARSING_INSTRUCTIONS,
    "output_format": OUTPUT_FORMATS,
    "example_output": EXAMPLE_OUTPUTS,
    "additional_guidelines": ADDITIONAL_GUIDELINES
}

@dataclass
class VAPromptComponents:
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