import streamlit as st

def apply_custom_theme():
    st.markdown("""
        <style>
        .main { background-color: #f9f9f9; }
        .stButton>button {
            border-radius: 8px;
            background-color: #2E86C1;
            color: white;
            font-weight: bold;
        }
        .stMetric {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)