# services/session_manager.py
# Simple Streamlit session helpers

import streamlit as st

def get_session_state(defaults: dict = None):
    defaults = defaults or {}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
    return st.session_state
