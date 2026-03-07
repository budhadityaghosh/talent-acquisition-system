import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from sourcing import candidate_form

st.title("📝 Candidate Application")

candidate_form.run()