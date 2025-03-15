from core.agent_factory import ConfigurableAgent
from core.rag_engine import ConfigurableRAG
from transformers import pipeline
from loguru import logger
import yaml

class MedicalTriageAgent:
    def __init__(self, agent_config: dict, rag_config: dict):  # Accept config dicts directly
        self.agent_config = agent_config
        self.rag_config = rag_config
        self.rag = ConfigurableRAG(rag_config)
        self.model = self._load_model()
        
    def _load_model(self):
        return pipeline(
            task="text-generation",
            model=self.agent_config["base_model"],
            device_map="auto",
            torch_dtype="auto"
        )
        
    def analyze(self, patient_input: str):
        try:
            # RAG Context Retrieval
            context = self.rag.query(patient_input)
            
            # Build structured prompt
            prompt = f"""
            MEDICAL TRIAGE ANALYSIS REQUEST:
            {patient_input}
            
            RELEVANT GUIDELINES:
            {context}
            
            REQUIRED OUTPUT FORMAT:
            {{
                "urgency": "emergent|urgent|non-urgent",
                "recommended_actions": [],
                "clinical_notes": ""
            }}
            """
            
            return self.agent.generate(prompt)
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {"error": "Analysis unavailable"}