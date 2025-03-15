#!/bin/bash

# Create data directories
mkdir -p data/{knowledge_base,models}

# Download sample medical documents
curl -o data/knowledge_base/emergency_guidelines.pdf \
https://example.com/sample_medical.pdf  # Replace with actual URL

# Pre-cache models
python -c "from transformers import AutoModel; AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')"