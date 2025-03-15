import sys
import os
import yaml
import torch
import gc
import time
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, TimeoutError

# Set page config FIRST AND ONLY ONCE
st.set_page_config(
    page_title="AI Triage Assistant",
    layout="wide",
    page_icon="🚑",
    menu_items={
        'Get Help': 'https://github.com/yourusername/Medical-Triage-Agent-Implementation',
        'Report a bug': "https://github.com/yourusername/Medical-Triage-Agent-Implementation/issues",
        'About': "AI-Powered Medical Triage Assistant v1.0"
    }
)

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import after page config
from core.workflows.medical_triage import MedicalTriageAgent
from core.responsible_ai import BiasDetector, PHIRedactor

# Initialize torch settings
torch.set_grad_enabled(False)

def inject_css():
    """Inject custom CSS styles"""
    with open("app/assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def show_guidelines():
    """Display ethical guidelines in sidebar"""
    with open("app/assets/guidelines.md") as f:
        st.sidebar.markdown(f.read())

def main():
    # Initialize UI components
    inject_css()
    show_guidelines()

    # Initialize session state components
    if "agent" not in st.session_state:
        with st.spinner("⚙️ Initializing AI components..."):
            # Load configurations
            with open("configs/agents/medical_triage.yaml") as f:
                agent_config = yaml.safe_load(f)
            
            with open("configs/rag_config.yaml") as f:
                rag_config = yaml.safe_load(f)
            
            # Initialize components
            st.session_state.redactor = PHIRedactor()
            st.session_state.bias_detector = BiasDetector()
            st.session_state.agent = MedicalTriageAgent(agent_config, rag_config)

    # Main UI
    st.title("🚑 AI-Powered Medical Triage Assistant")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Configuration")
        uploaded_files = st.file_uploader(
            "📤 Upload Medical Guidelines (PDF/TXT)",
            type=["pdf", "txt"],
            accept_multiple_files=True
        )
        
        # Handle document uploads
        if uploaded_files:
            save_dir = "data/knowledge_base/"
            os.makedirs(save_dir, exist_ok=True)
            
            for uploaded_file in uploaded_files:
                file_path = os.path.join(save_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            # Ingest documents with progress
            with st.spinner("📂 Processing documents..."):
                st.session_state.agent.rag.add_documents(save_dir)
            st.sidebar.success(f"✅ Processed {len(uploaded_files)} new documents!")

    # Main interface
    with st.container():
        user_input = st.text_area(
            "📝 Enter Patient Symptoms:",
            height=150,
            max_chars=500,
            placeholder="Example: 45yo male with crushing chest pain radiating to left arm..."
        )
        
        analyze_btn = st.button("🔍 Analyze", type="primary")

    # Analysis workflow
    if analyze_btn and user_input:
        progress_bar = st.progress(0)
        status_text = st.empty()
        result = None
        
        try:
            # Start timing
            start_time = time.time()
            MAX_WAIT = 35  # seconds (5s less than model timeout)
            
            # Redact PHI first
            status_text.markdown("🛡️ **Redacting sensitive information...**")
            clean_input = st.session_state.redactor.redact(user_input)
            progress_bar.progress(15)
            
            # Run analysis in thread with timeout
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    st.session_state.agent.analyze,
                    clean_input
                )
                
                # Update progress while waiting
                while not future.done():
                    elapsed = time.time() - start_time
                    progress = min(int((elapsed / MAX_WAIT) * 100), 95)
                    progress_bar.progress(progress)
                    status_text.markdown(f"🧠 **Analyzing symptoms ({progress}%)...**")
                    
                    if elapsed > MAX_WAIT:
                        future.cancel()
                        raise TimeoutError("Analysis timed out")
                    
                    time.sleep(0.2)
                
                # Get result
                result = future.result(timeout=MAX_WAIT)
                progress_bar.progress(100)
                status_text.markdown("✅ **Analysis complete**")
                time.sleep(0.5)

            # Display results
            if result.get("status") == "success":
                st.subheader("🩺 Triage Recommendation")
                st.json(result["medical_response"])
                
                # Show context documents
                with st.expander("📚 Reference Guidelines Used"):
                    for doc in result.get("context", []):
                        st.markdown(f"**Source**: {doc.metadata.get('source', 'Unknown')}")
                        st.text(doc.page_content[:500] + "...")
                
                # Responsible AI Dashboard
                st.subheader("🛡️ Responsible AI Analysis")
                col1, col2 = st.columns(2)
                
                with col1:
                    bias_result = st.session_state.bias_detector.analyze(
                        result["medical_response"]
                    )
                    st.metric(
                        "🤖 Bias Detection",
                        bias_result.get("bias_level", "N/A"),
                        delta=f"{bias_result.get('confidence', 0):.2f} confidence"
                    )
                
                with col2:
                    st.write("🔒 PHI Redaction Preview")
                    st.code(clean_input, language="text", line_numbers=True)

            else:
                st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

        except TimeoutError as te:
            st.error(f"""
            ⏳ **Analysis Timeout!**  
            Possible solutions:
            1. Use shorter symptom descriptions (<500 chars)
            2. Try a smaller AI model in config
            3. Add more medical guidelines
            4. Check system resources
            """)
            st.exception(te)
        except Exception as e:
            st.error(f"""
            ⚠️ **Critical System Error**  
            {str(e)}
            """)
            st.exception(e)
        finally:
            # Cleanup resources
            progress_bar.empty()
            status_text.empty()
            gc.collect()

if __name__ == "__main__":
    main()