import os
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Groq API key and model name from environment variables
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
MODEL_NAME = os.getenv('MODEL_NAME')

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
        "a concise, relevant reply that aligns with these goals."
    )

    try:
        # Invoke Llama model via Groq API
        response = llm.invoke(prompt)
        chatbot_response = response.content.strip()
        st.session_state.conversation_history.append(f"Chatbot: {chatbot_response}")
    except Exception as e:
        # Handle API errors
        st.session_state.conversation_history.append(f"Chatbot: Error occurred: {str(e)}")

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
                height: calc(100% - 60px); /* Adjust height based on input box height */
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
                padding: 10px;
                background-color: #fff;
                border-top: 1px solid #ddd;
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

    # Create chat layout with conversation history above input box
    chat_history_container = st.container()

    # Input container
    input_container = st.container()

    # Input container
    with input_container:
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="Enter your message", key="input_box")
            submit_button = st.form_submit_button("➤")

            if submit_button:
                # Exit conversation when user types 'bye'
                if user_input.lower() == "bye":
                    st.session_state.conversation_history.append("Chatbot: Goodbye! Take care!")
                    st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history after goodbye
                elif user_input:
                    # Generate chatbot response
                    chat_with_user(user_input)

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
