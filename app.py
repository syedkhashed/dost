import os
import random
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_keys_string = os.getenv('GROQ_API_KEYS')

# Split the string by newlines and remove any extra whitespace
api_keys_list = [key.strip() for key in api_keys_string.splitlines() if key.strip()]

# Select a random API key from the list
random_api_key = random.choice(api_keys_list)

MODEL_NAME = os.getenv('MODEL_NAME')
llm = ChatGroq(
    temperature=0.7,
    groq_api_key=random_api_key,
    model_name=MODEL_NAME
)

# Predefined initial message
INITIAL_MESSAGE = "Chatbot: Hi there! I'm here to listen and support you. How are you feeling right now?"

# Conversation history tracking
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = [INITIAL_MESSAGE]

chat_prompt = os.getenv("CHAT_PROMPT")

def chat_with_user(user_input):
    """Track conversation history and provide responses."""
    st.session_state.conversation_history.append(f"You: {user_input}")

    # Create prompt with the full conversation history
    conversation_history = "\n".join(st.session_state.conversation_history)
    prompt = chat_prompt.format(conversation_history=conversation_history)
    try:
        # Invoke Llama model via Groq API
        response = llm.invoke(prompt)
        chatbot_response = response.content.strip() if hasattr(response, 'content') else "Sorry, I didn't get that."
        st.session_state.conversation_history.append(f"Chatbot: {chatbot_response}")
    except Exception as e:
        # Handle API errors
        st.session_state.conversation_history.append(f"Chatbot: Error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="Chatbot", layout="wide")

    # Popup message for mobile users
    st.markdown(
        """
        <script>
            if (window.innerWidth <= 600) {
                alert('Kindly use desktop mode for better experience.');
            }
        </script>
        """,
        unsafe_allow_html=True
    )

    # Sidebar for navigation
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Select an option:", ["Home", "Feedback", "About"])

    # Apply styles
    st.markdown(f"""
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f0f4f8;
                color: #333;
                margin: 0;
                padding: 0;
                transition: background-color 0.3s ease;
            }}
            .header-container {{
                display: flex;
                align-items: center;
                padding: 10px;
                background-color: #87CEEB;
                border-bottom: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                background: none; /* Removed background color */
            }}
            .header-logo {{
                margin-right: 20px;
            }}
            .header-message {{
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
                color: #333;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}
            .chat-container {{
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
    if menu_option == "Home":
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
                if submit_button and user_input:
                    chat_with_user(user_input)

            if restart_button:
                st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history
                if restart_button:
                    st.session_state.conversation_history = [INITIAL_MESSAGE]  # Reset history

    # Display conversation history in the chat history container
    with chat_history_container:
        chat_history = ""
        for line in reversed(st.session_state.conversation_history):
            if line.startswith("You:"):
                chat_history += f'<div class="chat-message user">{line}</div>'
            else:
                chat_history += f'<div class="chat-message bot">{line}</div>'
        st.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)
        # Display conversation history in the chat history container
        with chat_history_container:
            chat_history = ""
            for line in reversed(st.session_state.conversation_history):
                if line.startswith("You:"):
                    chat_history += f'<div class="chat-message user">{line}</div>'
                else:
                    chat_history += f'<div class="chat-message bot">{line}</div>'
            st.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

    if menu_option == "Feedback":
    elif menu_option == "Feedback":
        # Feedback section
        st.header("Feedback")
        st.write("We value your feedback! Please let us know your thoughts about the chatbot.")

        feedback = st.text_area("Your Feedback:", "")

        if st.button("Generate Feedback Link"):
            if feedback:
                feedback_link = f"mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body={feedback}"
                st.markdown(f'<a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>', unsafe_allow_html=True)
            else:
                st.error("Please enter your feedback before sending.")

    elif menu_option == "About":
        # Updated About section
        st.header("About")
        st.write("""
        Welcome to our chatbot! This virtual friend is here to provide support for your mental health. 
        You can share your thoughts and feelings in a safe and non-judgmental environment. 
        Our aim is to listen and offer guidance to help you navigate life's challenges.
        """)

if __name__ == "__main__":
    main()
    
