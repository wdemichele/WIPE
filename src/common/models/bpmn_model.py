from dataclasses import dataclass

@dataclass
class BPMNModel:
    name: str
    model: str
        
    @classmethod
    def from_text(cls, file_path: str) -> 'BPMNModel':
        # Load text file
        with open(file_path, 'r') as file:
            text = file.read()
        
        name = file_path.split('\\')[-2]
        bpmn_model = cls(name, text)
        
        return bpmn_model
    
    @classmethod
    def from_str(cls, name: str, model: str) -> 'BPMNModel':
        return cls(name, model)