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
                color: #333;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
            }}
            .chat-container {{
                display: flex;
                flex-direction: column;
                height: 80vh;
                border: 1px solid #ddd;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .chat-history {{
                flex: 1;
                overflow-y: auto;
                padding: 10px;
                display: flex;
                flex-direction: column-reverse;
                justify-content: flex-start;
                scrollbar-width: thin; /* Firefox */
                scrollbar-color: #888 #f1f1f1; /* Firefox */
            }}
            .chat-history::-webkit-scrollbar {{
                width: 8px;
            }}
            .chat-history::-webkit-scrollbar-track {{
                background: #f1f1f1;
            }}
            .chat-history::-webkit-scrollbar-thumb {{
                background: #888;
                border-radius: 10px;
            }}
            .chat-message {{
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
                transition: background-color 0.3s, transform 0.2s;
                animation: fadeIn 0.5s ease;
            }}
            .chat-message.user {{
                align-self: flex-end;
                background-color: #e1ffc7; /* Light green for user */
                color: #000;
            }}
            .chat-message.bot {{
                align-self: flex-start;
                background-color: #d9edf7; /* Light blue for bot */
                color: #000;
            }}
            .input-container {{
                padding: 10px;
                background-color: #ffffff;
                border-top: 1px solid #ddd;
                display: flex;
                flex-direction: column;
            }}
            .input-container input {{
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                width: 100%;
                transition: border 0.3s;
            }}
            .input-container input:focus {{
                border: 1px solid #87CEEB;
                outline: none;
            }}
            .input-container button {{
                padding: 15px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
                color: white !important;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                background-color: #87CEEB;
            }}
            .input-container button:hover {{
                background-color: #00BFFF !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }}
            .feedback-button {{
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
            }}
            .feedback-button:hover {{
                background-color: #00BFFF !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }}
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                }}
                to {{
                    opacity: 1;
                }}
            }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="header-container">
        <div class="header-logo">
            <img src='https://imgur.com/nnZtupY.png' width="100" alt="Logo">
        </div>
        <div class="header-message">Welcome to the chatbot!</div>
    </div>""", unsafe_allow_html=True)

    # Create chat layout with conversation history above input box
    chat_history_container = st.container()
    input_container = st.container()

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
