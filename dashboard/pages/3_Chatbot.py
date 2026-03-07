import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from engagement import chatbot

st.title("💬 AI HR Chatbot")

chatbot.run()