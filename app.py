import os
import random
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API keys as a single string from the environment variable
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
            }
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
            .chat-history {
                height: 70vh;
                overflow-y: auto;
                padding: 10px;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
                border-radius: 8px;
                margin-bottom: 10px;
            }
            .chat-message {
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .chat-message.user {
                background-color: #e1ffc7;
                align-self: flex-end;
            }
            .chat-message.bot {
                background-color: #d9edf7;
                align-self: flex-start;
            }
            .input-container {
                display: flex;
            }
            .input-container input {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 10px;
                flex: 1;
            }
            .input-container button {
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                background-color: #87CEEB;
                color: white;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            .input-container button:hover {
                background-color: #00BFFF;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown("""<div class="header-container">
        <div class="header-logo">
            <img src='https://imgur.com/nnZtupY.png' width="100" alt="Logo">
        </div>
        <div class="header-message">Welcome to the chatbot!</div>
    </div>""", unsafe_allow_html=True)

    chat_history = st.container()
    input_container = st.container()

    with chat_history:
        for line in st.session_state.conversation_history:
            if line.startswith("You:"):
                st.markdown(f'<div class="chat-message user">{line}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot">{line}</div>', unsafe_allow_html=True)

    with input_container:
        user_input = st.text_input("Enter your message:", placeholder="Type here...", key="input_box")
        col1, col2 = st.columns([2, 1])
        with col1:
            submit_button = st.button("➤", key="send_button")
        with col2:
            restart_button = st.button("⟳", key="restart_button")

        if submit_button and user_input:
            chat_with_user(user_input)
            st.session_state.input_box = ""  # Clear input

        if restart_button:
            st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history

if __name__ == "__main__":
    main()
