from core.agent_factory import ConfigurableAgent

class FinancialAnalyst:
    def __init__(self, config_path):
        self.agent = ConfigurableAgent(config_path)
        
    def analyze_statement(self, text: str):
        prompt = f"""
        Analyze financial statement:
        {text}
        
        Identify:
        - Revenue trends
        - Risk factors
        - Anomalies
        """
        return self.agent.generate(prompt)