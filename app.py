import os
import random
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_keys_string = os.getenv('GROQ_API_KEYS')
api_keys_list = [key.strip() for key in api_keys_string.splitlines() if key.strip()]
random_api_key = random.choice(api_keys_list)

MODEL_NAME = os.getenv('MODEL_NAME')
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=random_api_key,
    model_name=MODEL_NAME
)

INITIAL_MESSAGE = "Chatbot: Hi there! I'm here to listen and support you. How are you feeling right now?"

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [INITIAL_MESSAGE]

chat_prompt = os.getenv("CHAT_PROMPT")

def chat_with_user(user_input):
    st.session_state.conversation_history.append(f"You: {user_input}")
    conversation_history = "\n".join(st.session_state.conversation_history)
    prompt = chat_prompt.format(conversation_history=conversation_history)
    try:
        response = llm.invoke(prompt)
        chatbot_response = response.content.strip() if hasattr(response, 'content') else "Sorry, I didn't get that."
        st.session_state.conversation_history.append(f"Chatbot: {chatbot_response}")
    except Exception as e:
        st.session_state.conversation_history.append(f"Chatbot: Error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="Chatbot", layout="wide")

    st.write(
        """
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background: linear-gradient(135deg, #f3f4f6, #e2e8f0);
            }
            .header-container {
                display: flex;
                align-items: center;
                padding: 15px;
                background-color: #ffffff;
                border-bottom: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header-logo {
                margin-right: 15px;
            }
            .header-message {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
            }
            .chat-container {
                display: flex;
                flex-direction: column;
                height: 80vh;
                border: 1px solid #ddd;
                border-radius: 12px;
                overflow: hidden;
                background-color: #ffffff;
                transition: box-shadow 0.3s;
            }
            .chat-container:hover {
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
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
                padding: 10px;
                border-radius: 12px;
                max-width: 80%;
                word-wrap: break-word;
                transition: background-color 0.3s, transform 0.3s;
            }
            .chat-message.user {
                align-self: flex-end;
                background-color: #d1fae5; /* Light green for user */
                color: #000;
            }
            .chat-message.bot {
                align-self: flex-start;
                background-color: #e0f2fe; /* Light blue for bot */
                color: #000;
            }
            .chat-message:hover {
                transform: scale(1.02);
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
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-bottom: 10px;
                width: 100%;
                font-size: 16px;
            }
            .input-container button {
                padding: 15px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                color: white !important;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                flex: 1;
                position: relative;
            }
            .input-container button.send-button {
                background-color: #3b82f6 !important;
            }
            .input-container button.send-button:hover {
                background-color: #2563eb !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .input-container button.restart-button {
                background-color: #4ade80 !important;
            }
            .input-container button.restart-button:hover {
                background-color: #22c55e !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .feedback-button {
                background-color: #3b82f6 !important;
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
                background-color: #2563eb !important;
                color: white !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            @media (max-width: 600px) {
                .header-message {
                    font-size: 20px;
                }
                .input-container input {
                    font-size: 14px;
                }
                .chat-message {
                    font-size: 14px;
                }
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Header with logo and welcome message
    st.markdown("""<div class="header-container">
        <div class="header-logo">
            <img src='https://imgur.com/nnZtupY.png' width="100" alt="Logo">
        </div>
        <div class="header-message">Welcome to the chatbot!</div>
    </div>""", unsafe_allow_html=True)

    # Create chat layout with conversation history above input box
    chat_history_container = st.container()
    input_container = st.container()

    # Input container
    with input_container:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Enter your message", key="input_box")
            col1, col2 = st.columns([2, 1])
            with col1:
                submit_button = st.form_submit_button("➤", key="send_button")  # Send button
            with col2:
                restart_button = st.form_submit_button("⟳", key="restart_button")  # Restart button

            if submit_button and user_input:
                chat_with_user(user_input)

            if restart_button:
                st.session_state.conversation_history = [INITIAL_MESSAGE]

    # Feedback button outside the form
    st.markdown("""<a href="mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body=Please provide your feedback here."
       class="feedback-button">📧 Feedback</a>""", unsafe_allow_html=True)

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
