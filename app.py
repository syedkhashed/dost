


import os
import streamlit as st
from langchain_groq import ChatGroq

# Load Groq API key and model name from environment variables
GROQ_API_KEY = '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'
MODEL_NAME = "llama-3.1-70b-versatile"

# Initialize the Llama 3.1 model using Groq API
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

    # Modify prompt to better understand user's problem and emotions
    prompt = (
        "The user said: {}. Understand user's emotion, feelings, and mental state "
        "by getting more details, interacting friendly and comfortably with words, "
        "generate proverbs and quotes according to the situation, considering human psychology. "
        "Generate the response thinking it was given to user and do not generate large responses."
    ).format(user_input)

    try:
        # Invoke Llama model via Groq API
        response = llm.invoke(prompt)
        st.session_state.conversation_history.append(f"Chatbot: {response.content}")
        return response.content
    except Exception as e:
        # Handle API errors
        return f"Error: {str(e)}"

def main():
    st.title("Welcome to the chatbot!")
    st.write("Type 'stop' to exit.")

    # Custom CSS for chat layout
    st.markdown("""
        <style>
            .chat-container {
                display: flex;
                flex-direction: column;
                height: 80vh;
                overflow: hidden;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
            }
            .chat-history {
                flex: 1;
                overflow-y: auto;
                padding: 10px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
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
                display: flex;
                border-top: 1px solid #ddd;
                padding: 10px;
                background-color: #fff;
                position: fixed;
                bottom: 0;
                width: 100%;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                z-index: 1;
            }
            .input-container input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Create chat layout
    chat_history_container = st.container()
    input_container = st.container()

    # Display conversation history
    with chat_history_container:
        st.markdown("")  # Create an empty container to hold chat history

    # Input container
    with input_container:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Enter your message", key="input_box")
            submit_button = st.form_submit_button("Send")

            if submit_button:
                # Exit conversation when user types 'stop'
                if user_input.lower() == "stop":
                    st.session_state.conversation_history.append("Chatbot: Goodbye! Take care!")
                    st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history after goodbye
                # Validate user input
                elif user_input:
                    # Generate chatbot response
                    response = chat_with_user(user_input)

                # Refresh chat history container
                with chat_history_container:
                    st.markdown("")  # Clear the previous display
                    # Display chat history in chronological order
                    for line in st.session_state.conversation_history:
                        if line.startswith("You:"):
                            st.markdown(f'<div class="chat-message user">{line}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="chat-message bot">{line}</div>', unsafe_allow_html=True)
                    st.experimental_rerun()  # Force a rerun to refresh the chat history

if __name__ == "__main__":
    main()

