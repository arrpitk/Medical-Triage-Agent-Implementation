from core.agent_factory import ConfigurableAgent
from core.rag_engine import ConfigurableRAG
from loguru import logger

class MedicalTriageAgent:
    def __init__(self, agent_config: str, rag_config: dict):
        self.agent = ConfigurableAgent(agent_config)
        self.rag = ConfigurableRAG(rag_config)
        
    def load_knowledge(self, documents: list):
        self.rag.add_documents(documents)
        
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