# Add to imports
import base64
import yaml
import torch
torch.set_grad_enabled(False)

# Add after imports
def inject_css():
    with open("app/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_guidelines():
    with open("app/assets/guidelines.md") as f:
        st.sidebar.markdown(f.read())

# Modify main()
def main():
    inject_css()
    show_guidelines()
    # Rest of existing code

import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import streamlit as st
from core.workflows.medical_triage import MedicalTriageAgent
from core.responsible_ai import BiasDetector, PHIRedactor

import json

# Initialize components
redactor = PHIRedactor()
bias_detector = BiasDetector()

def main():
    
    # Load configurations first
    with open("configs/agents/medical_triage.yaml") as f:
        agent_config = yaml.safe_load(f)

    with open("configs/rag_config.yaml") as f:
        rag_config = yaml.safe_load(f)

    # Initialize components
    agent = MedicalTriageAgent(agent_config, rag_config)
    st.set_page_config(page_title="Medical Triage Agent", layout="wide")
    
    # Sidebar Controls
    st.sidebar.header("Configuration")
    uploaded_files = st.sidebar.file_uploader(
        "Upload Medical Guidelines", 
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    # Main Interface
    st.title("AI-Powered Medical Triage Assistant")
    user_input = st.text_area("Patient Symptoms:", height=150)
    
    if st.button("Analyze"):
        with st.spinner("Processing..."):
            # Initialize Agent
            # Load configurations first
            
    
            

# Initialize agent with config dicts
            
            
            # Redact PHI
            clean_input = redactor.redact(user_input)
            
            # Process Analysis
            result = agent.analyze(clean_input)
            
            # Display Results
            st.subheader("Triage Recommendation")
            st.json(result["medical_response"])
            
            # Responsible AI Dashboard
            st.subheader("Responsible AI Analysis")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Bias Detection", 
                          result["bias_check"]["bias_level"],
                          delta=f"{result['bias_check']['confidence']:.2f} confidence")
                
            with col2:
                st.write("**PHI Redaction Preview**")
                st.code(clean_input, language="text")
            
            # Explanation Visualization
            st.plotly_chart(
                plot_feature_importance(result["explanation"])
            )

def plot_feature_importance(explanation):
    # Visualization code using Plotly
    pass

if __name__ == "__main__":
    main()