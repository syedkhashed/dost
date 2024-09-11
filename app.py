import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Groq API key and model name from environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')


llm = ChatGroq(
    temperature=0.7,
    groq_api_key=GROQ_API_KEY,
    model_name=MODEL_NAME
)

# Predefined initial message
INITIAL_MESSAGE = "Chatbot: Hi there! I'm here to listen and support you. How are you feeling today?"

# Conversation history tracking
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [INITIAL_MESSAGE]

def chat_with_user(user_input):
    """Track conversation history, understand user's emotions and feelings, and provide motivational suggestions."""
    st.session_state.conversation_history.append(f"You: {user_input}")

    # Create prompt with the full conversation history
    conversation_history = "\n".join(st.session_state.conversation_history)
    prompt = (
        f"Here is the conversation history:\n{conversation_history}\n\n"

"Respond to the latest user input by considering the entire conversation history. Focus on these key aspects:"

"1. Understanding Emotions: Accurately assess and acknowledge the user's current emotions and mental state. Show deep empathy and validate their feelings by reflecting their experiences back to them in a compassionate manner."

"2. Uplifting and Comforting: Aim to uplift the user's mood and provide comfort. Your response should be encouraging and supportive, offering reassurance and positive reinforcement."

"3. Building Trust: Use warm, non-judgmental language to build trust and rapport with the user. Ensure your tone fosters a safe and supportive environment where the user feels heard and valued."

"4. Original Quote or Proverb: Include a unique, original quote or proverb that aligns with the user's situation. Ensure it is inspiring, relevant, and crafted specifically for the user’s context."

"5. Small Length: Craft your response to be of small length—comprehensive enough to provide meaningful support and insight, yet concise enough to keep the user engaged without overwhelming them."

"Your response should integrate these elements seamlessly, creating a supportive, empathetic, and engaging interaction tailored to the user’s needs."
    )

    try:
        # Invoke Llama model via Groq API
        response = llm.invoke(prompt)
        chatbot_response = response.content.strip() if hasattr(response, 'content') else "Sorry, I didn't get that."
        st.session_state.conversation_history.append(f"Chatbot: {chatbot_response}")
    except Exception as e:
        # Handle API errors
        st.session_state.conversation_history.append(f"Chatbot: Error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="Chatbot", layout="wide")  # Set wide mode

    st.write(
        """
        <style>
            .header-container {
                display: flex;
                align-items: center;
                padding: 10px;
                background-color: #f1f1f1;
                border-bottom: 1px solid #ddd;
            }
            .header-logo {
                margin-right: 20px;
            }
            .header-message {
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }
            .chat-container {
                display: flex;
                flex-direction: column;
                height: 80vh;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
            }
            .chat-history {
                flex: 1;
                overflow-y: auto;
                padding: 10px;
                display: flex;
                flex-direction: column-reverse;
                justify-content: flex-start;
            }
            .chat-message {
                margin-bottom: 10px;
            }
            .chat-message.user {
                text-align: right;
                color: #007bff;
            }
            .chat-message.bot {
                text-align: left;
                color: #28a745;
            }
            .input-container {
                padding: 10px;
                background-color: #fff;
                border-top: 1px solid #ddd;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                z-index: 1;
                display: flex;
                flex-direction: column;
            }
            .input-container input {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                width: 100%; /* Ensure input box is full width */
            }
            .button-container {
                display: flex;
                flex-wrap: wrap; /* Allows buttons to wrap on smaller screens */
                gap: 10px; /* Space between buttons */
            }
            .input-container button {
                padding: 10px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: white !important;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .input-container button.send-button {
                background-color: #87CEEB !important;
                flex: 1; /* Allow button to grow */
            }
            .input-container button.send-button:hover {
                background-color: #00BFFF !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .input-container button.restart-button {
                background-color: #28a745 !important;
                flex: 1; /* Allow button to grow */
            }
            .input-container button.restart-button:hover {
                background-color: #218838 !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .feedback-button {
                background-color: #87CEEB !important;
                color: white !important;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                margin-top: 15px;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .feedback-button:hover {
                background-color: #00BFFF !important;
                color: white !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Header with logo and welcome message
    st.markdown("""
        <div class="header-container">
            <div class="header-logo">
                <img src="https://i.imgur.com/fdGSoqQ.png" width="75" alt="Logo">
            </div>
            <div class="header-message">Welcome to the chatbot!</div>
        </div>
    """, unsafe_allow_html=True)

    # Create chat layout with conversation history above input box
    chat_history_container = st.container()
    input_container = st.container()

    # Input container
    with input_container:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Enter your message", key="input_box")
            col1, col2 = st.columns([2, 1])
            with col1:
                submit_button = st.form_submit_button("➤")  # Send button
            with col2:
                restart_button = st.form_submit_button("⟳")  # Restart button

            if submit_button and user_input:
                chat_with_user(user_input)

            if restart_button:
                st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history

    # Feedback button outside the form
    st.markdown("""
        <a href="mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body=Please provide your feedback here."
           class="feedback-button">📧 Feedback</a>
    """, unsafe_allow_html=True)

    # Display conversation history in the chat history container
    with chat_history_container:
        chat_history = ""
        for line in reversed(st.session_state.conversation_history):
            if line.startswith("You:"):
                chat_history += f'<div class="chat-message user">{line}</div>'
            else:
                chat_history += f'<div class="chat-message bot">{line}</div>'
        st.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

