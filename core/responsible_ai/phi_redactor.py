import re

class PHIRedactor:
    def __init__(self):
        self.patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{4} \d{4} \d{4} \d{4}\b",  # Credit Card
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"  # Email
        ]
    
    def redact(self, text: str) -> str:
        for pattern in self.patterns:
            text = re.sub(pattern, "[REDACTED]", text)
        return text
