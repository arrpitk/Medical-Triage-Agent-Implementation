import yaml
from transformers import pipeline
from typing import Dict, Any

class ConfigurableAgent:
    def __init__(self, config_path: str):
        self.config = self._load_config(config_path)
        self.model = self._load_model()
        
    def _load_config(self, path: str) -> Dict[str, Any]:
        with open(path) as f:
            return yaml.safe_load(f)
    
    def _load_model(self):
        return pipeline(
            task="text-generation",
            model=self.config["base_model"],
            device_map="auto",
            load_in_8bit=True,
            torch_dtype="auto"
        )
    
    def generate(self, prompt: str):
        return self.model(
            prompt,
            max_new_tokens=self.config["max_token_limit"]
        )[0]['generated_text']