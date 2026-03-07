import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from screening import screening_results

st.title("🤖 AI Resume Screening")

screening_results.run()