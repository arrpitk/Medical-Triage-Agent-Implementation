import shap
import numpy as np

class ExplanationGenerator:
    def __init__(self, model, tokenizer):
        self.explainer = shap.Explainer(model, tokenizer)
        
    def generate_explanation(self, text: str) -> dict:
        shap_values = self.explainer([text])
        return {
            "feature_importance": {
                str(f): float(v) 
                for f, v in zip(shap_values.data[0], shap_values.values[0].mean(0))
            },
            "base_value": float(shap_values.base_values[0].mean())
        }
