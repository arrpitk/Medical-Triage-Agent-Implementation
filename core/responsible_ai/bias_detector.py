from transformers import pipeline
import logging

class BiasDetector:
    def __init__(self):
        self.detector = pipeline(
            "text-classification", 
            model="valurank/bias-detection",
            device_map="auto",
            torch_dtype="auto"
        )
    
    def analyze(self, text: str) -> dict:
        try:
            result = self.detector(text[:512])[0]  # Truncate for performance
            return {
                "bias_level": result["label"],
                "confidence": float(result["score"])
            }
        except Exception as e:
            logging.error(f"Bias detection failed: {str(e)}")
            return {"error": "Bias analysis unavailable"}
