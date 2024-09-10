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
        "Respond to the latest user input considering the entire conversation history. "
        "Understand the user's emotions, feelings, and mental state by interacting in a friendly, empathetic, "
        "and supportive manner. Tailor your response to build trust and provide comfort. "
        "Include a single relevant proverb or quote according to the user's situation, without mentioning the author. "
        "Ensure the proverb or quote is uplifting and appropriate. Make sure your response is non-judgmental and respectful, "
        "fostering a safe and inclusive environment. Use insights from human psychology to guide your response, and generate "
        "a concise, relevant reply that aligns with these goals and generate precise response by interacting to get more information.and do not generate large responses"
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
            }
            .input-container button {
                padding: 10px;
                border: none;
                border-radius: 8px; /* Rounded corners */
                font-size: 16px; /* Font size */
                font-weight: bold; /* Bold text */
                color: white !important; /* White text */
                cursor: pointer; /* Pointer cursor on hover */
                margin-right: 5px;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; /* Smooth transition */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            .input-container button.send-button {
                background-color: #87CEEB !important; /* Sky blue background */
            }
            .input-container button.send-button:hover {
                background-color: #00BFFF !important; /* Brighter blue on hover */
                transform: scale(1.05); /* Slightly larger on hover */
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Enhanced shadow on hover */
            }
            .input-container button.restart-button {
                background-color: #28a745 !important; /* Green background */
            }
            .input-container button.restart-button:hover {
                background-color: #218838 !important; /* Darker green on hover */
                transform: scale(1.05); /* Slightly larger on hover */
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Enhanced shadow on hover */
            }
            .feedback-button {
                background-color: #87CEEB !important; /* Sky blue background */
                color: white !important; /* White text */
                border: none; /* No borders */
                border-radius: 8px; /* Rounded corners */
                padding: 12px 24px; /* Increased padding */
                text-align: center; /* Centered text */
                text-decoration: none; /* No underline */
                display: inline-block; /* Inline-block display */
                font-size: 18px; /* Larger font size */
                font-weight: bold; /* Bold text */
                cursor: pointer; /* Pointer cursor on hover */
                margin-top: 15px; /* Top margin */
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s; /* Smooth transition */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Subtle shadow */
            }
            .feedback-button:hover {
                background-color: #00BFFF !important; /* Brighter blue on hover */
                color: white !important; /* Ensure text remains white on hover */
                transform: scale(1.05); /* Slightly larger on hover */
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3); /* Enhanced shadow on hover */
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
