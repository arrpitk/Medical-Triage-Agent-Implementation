from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import torch

class MedicalTriageAgent:
    def __init__(self, agent_config: dict, rag_config: dict):
        # Load model with CPU optimizations
        self.model = AutoModelForCausalLM.from_pretrained(
            agent_config["base_model"],
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            agent_config["base_model"]
        )
        self.rag = ConfigurableRAG(rag_config)

    def analyze(self, patient_input: str):
        inputs = self.tokenizer(
            patient_input,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True
            )
            
        return {
            "medical_response": self.tokenizer.decode(outputs[0]),
            "status": "success"
        }