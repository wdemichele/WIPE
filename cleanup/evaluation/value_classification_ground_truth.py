import json
from typing import Dict
from src.process.activity import Activity

class ValueClassificationGroundTruth:
    def __init__(self, data: Dict):
        if "activities" in data:
            data = data["activities"]
        self.activities = [Activity(**activity) for activity in data]

    @classmethod
    def from_json(cls, json_data: str):
        return cls(json.loads(json_data))