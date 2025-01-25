import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Keshava AI - Your Spiritual Guide",
    page_icon="🕉️",
    layout="centered"
)

# Add custom CSS
st.markdown("""
    <style>
        .stTextInput > div > div > input {
            background-color: #f0f2f6;
        }
        .stButton > button {
            background-color: #ff6b6b;
            color: white;
            border-radius: 5px;
        }
        .stButton > button:hover {
            background-color: #ff5252;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            flex-direction: column;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
            align-self: flex-start;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Gemini AI
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    st.error("No Google API key found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display header
st.title("🕉️ Keshava AI")
st.markdown("### Your Spiritual Guide and Knowledge Companion")
st.markdown("---")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">Keshava: {message["content"]}</div>', unsafe_allow_html=True)

# Chat input
user_input = st.text_input("Type your message here...", key="user_input")

if st.button("Send") or user_input:
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Create chat with Keshava AI persona
            chat = model.start_chat(history=[])
            system_prompt = """You are Keshava AI, a friendly and knowledgeable assistant with deep understanding of Indian culture, 
            philosophy, and spirituality. You communicate with warmth and wisdom, often incorporating relevant references to ancient 
            Indian texts and teachings when appropriate. You are helpful, respectful, and aim to provide meaningful insights while 
            maintaining a connection to Indian values and traditions."""
            
            # Get response from AI
            response = chat.send_message(f"{system_prompt}\n\nUser message: {user_input}")
            
            # Add AI response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
            # Clear input
            st.session_state.user_input = ""
            
            # Rerun to update chat display
            st.rerun()
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Made with ❤️ and spiritual wisdom")
