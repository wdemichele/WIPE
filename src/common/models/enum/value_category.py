from enum import Enum

class ValueCategory(Enum):
    VALUE_ADDING = "VA"  # Value-adding steps = Directly contribute to positive outcomes of the process.
    BUSINESS_VALUE_ADDING = "BVA"  # Business value-adding steps = Steps that are necessary or useful for the company that performs the process.
    NON_VALUE_ADDING = "NVA"  # Non-value-adding steps = Steps that do not add value to the process.