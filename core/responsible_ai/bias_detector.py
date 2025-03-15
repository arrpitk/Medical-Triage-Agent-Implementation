from transformers import pipeline

class BiasDetector:
    def __init__(self):
        self.detector = pipeline("text-classification", model="valurank/distilroberta-bias")
    
    def analyze(self, text: str) -> dict:
        try:
            result = self.detector(text[:512])[0]
            return {
                "bias_level": result["label"],
                "confidence": float(result["score"])
            }
        except Exception as e:
            return {"error": str(e)}