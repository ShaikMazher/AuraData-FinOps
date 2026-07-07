import streamlit as st
from finops_agent import run_finops_analysis
from PIL import Image

# 1. Page Configuration
logo = Image.open("image_6.png")
st.set_page_config(page_title="AuraData FinOps", page_icon=logo, layout="wide")

# 2. Premium "Dark Mode" CSS (Fixed Text Colors)
st.markdown("""
    <style>
    /* Force App Background to Dark */
    .stApp { background-color: #0e1117; }
    
    /* Force Text to White for visibility */
    .stApp, .stApp p, .stApp span, .stApp label, h1, h2, h3, h4, h5, h6, [data-testid="stMetricValue"], [data-testid="stMetricLabel"] { 
        color: #f8fafc !important; 
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #1f2937; }
    
    /* Blend the logo perfectly */
    img { mix-blend-mode: screen; border-radius: 0px; }
    
    /* Premium Button */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background-color: #ffffff !important; 
        color: #000000 !important; 
        font-weight: 800; 
        border: none; 
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #cccccc !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.image(logo, width=200) 
    st.info("Capstone: Agents for Business\nTrack: Google Gemini 2.5 Flash")
    st.divider()
    st.write("**Tech Stack:**\n- FastMCP Server\n- SQLite Database\n- Agentic Tool Calling")

# 4. Main Dashboard Header 
col1, col2, col3 = st.columns([1, 1.5, 1]) 
with col2:
    # FIXED: Changed to use_container_width to clear the warning
    st.image(logo, use_container_width=True) 
    
st.markdown("<h4 style='text-align: center; color: #a1a1aa; margin-top: -30px;'>Secure Cloud Cost Intelligence & Policy Enforcement</h4>", unsafe_allow_html=True)
st.divider()

# 5. Top-Level Metric Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Monthly Spend", value="$101,601", delta="-2.4% vs Last Month")
with col2:
    st.metric(label="Top Department", value="Engineering")
with col3:
    st.metric(label="Optimization Potential", value="35%", delta="High Priority", delta_color="inverse")

st.divider()

# 6. Interaction Area
st.subheader("🤖 AI Agent Command Center")
user_input = st.text_input("Instruct AuraData to analyze specific costs:", 
                          "Run a SELECT * query. Which department is spending the most and how can we optimize AWS EC2 costs?")

if st.button("Generate Executive Analysis"):
    with st.spinner("Agent authenticating with MCP Server..."):
        try:
            report = run_finops_analysis(user_input)
            st.success("Analysis Delivered Successfully")
            
            with st.container():
                st.markdown("### 📝 Executive Summary")
                st.write(report)
        except Exception as e:
            st.error(f"System Error: {e}")

st.divider()
st.caption("AuraData Agentic Workflow - Secured by Policy-Based Access Control (PBAC)")