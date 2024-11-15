import re
from typing import List, Dict
from src.common.models.enum.value_category import ValueCategory

class ValueClassificationGPTResponse:
    def __init__(self, response: str):
        self.classifications = self._parse_response(response)

    def _parse_response(self, response: str) -> List[Dict]:
        pattern = r'classify_(\w+)\("([^"]+)", "([^"]+)", "([^"]+)"\)'
        matches = re.findall(pattern, response)
        return [
            {
                'category': self._map_category(match[0]),
                'step': match[1],
                'description': match[2],
                'reasoning': match[3]
            }
            for match in matches
        ]

    def _map_category(self, category: str) -> ValueCategory:
        if category == 'value_adding':
            return ValueCategory.VALUE_ADDING
        elif category == 'business_value_adding':
            return ValueCategory.BUSINESS_VALUE_ADDING
        else:
            return ValueCategory.NON_VALUE_ADDING