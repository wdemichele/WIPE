OUTPUT_FORMATS = {
    "standard_output": """Your response should follow this structure:
```json
{
    "activity_breakdown": [
        {
            "activity_name": "Name of the activity",
            "substeps": [
                {"step_number": 1, "description": "Brief description of substep 1"},
                {"step_number": 2, "description": "Brief description of substep 2"},
                ...
            ]
        },
        ...
    ]
}
```
"""
}
