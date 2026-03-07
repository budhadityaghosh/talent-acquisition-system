import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from engagement.pages import scheduler

st.title("📅 Interview Scheduler")

scheduler.run()