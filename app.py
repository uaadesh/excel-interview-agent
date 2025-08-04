# app.py
"""
This is the main entry point for the Streamlit web application.
It handles the user interface, state management, and interaction with the
ExcelInterviewerAgent.
"""
import streamlit as st
from agent import ExcelInterviewerAgent
from prompts import get_welcome_prompt

# --- Constants and Configuration ---
# This configuration defines the structure of the interview.
# It's defined here for easy modification.
INTERVIEW_CONFIG = {'easy': 2, 'medium': 2, 'hard': 1}

# --- Page Configuration ---
st.set_page_config(
    page_title="Excellytix AI Interviewer",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="auto"
)

st.title("🤖 Excellytix AI Mock Interview")

# --- State Initialization ---
# Streamlit's session_state is used to persist the agent and UI state
# across user interactions (which cause the script to rerun).
if "agent" not in st.session_state:
    # This block runs only once at the beginning of a user's session.
    st.session_state.agent = ExcelInterviewerAgent(interview_config=INTERVIEW_CONFIG)
    st.session_state.interview_started = False
    st.session_state.show_next_btn = False
    
    # The agent's history is initialized with the welcome message.
    welcome_msg = get_welcome_prompt(len(st.session_state.agent.interview_playlist))
    st.session_state.agent.history.append({"role": "assistant", "content": welcome_msg})

# --- UI Rendering ---
# The chat history is displayed on every script rerun to keep the UI updated.
for message in st.session_state.agent.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Main Application Logic (State Machine) ---
# The application's behavior is determined by the agent's current state.

# State 1: Conclusion
if st.session_state.agent.state == "CONCLUSION":
    st.info("The interview has concluded. See your performance summary above.")
    if st.button("Restart Interview"):
        st.session_state.clear()  # Clear the entire session for a fresh start.
        st.rerun()

# State 2: Introduction (Interview not yet started)
elif not st.session_state.interview_started:
    if st.button("Start Interview"):
        st.session_state.interview_started = True
        with st.spinner("Starting..."):
            st.session_state.agent.start_interview()
        st.rerun() # Rerun to display the first question.

# State 3: Interview in Progress (Evaluating)
else:
    # This block manages the interaction during a question.
    if st.session_state.show_next_btn:
        # If true, hide the chat input and show only the "Next Question" button.
        if st.button("Next Question"):
            st.session_state.show_next_btn = False
            with st.spinner("Loading next question..."):
                st.session_state.agent.get_next_question()
            st.rerun()
    else:
        # Show the chat input and wait for the user's answer.
        if user_input := st.chat_input("Your formula or explanation..."):
            with st.spinner("Evaluating..."):
                response = st.session_state.agent.process_user_response(user_input)
            
            # After processing, decide if the "Next Question" button should be shown.
            # This happens if the user was correct OR if they've used all their attempts.
            if response.get("is_correct") or response.get("attempts", 0) >= 2:
                st.session_state.show_next_btn = True

            st.rerun() # Rerun to display the new messages and potentially the "Next Question" button.