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

    # Theme switching
    theme = st.sidebar.selectbox("Select Theme:", ["Light", "Dark"])

    # Apply styles based on selected theme
    if theme == "Dark":
        bg_color = "#2E2E2E"
        text_color = "#FFFFFF"
        input_bg_color = "#444444"
        button_color = "#4CAF50"
    else:
        bg_color = "#F9F9F9"
        text_color = "#333333"
        input_bg_color = "#FFFFFF"
        button_color = "#87CEEB"

    st.markdown(f"""
        <style>
            body {{
                background-color: {bg_color};
                color: {text_color};
            }}
            .header-container {{
                display: flex;
                align-items: center;
                padding: 10px;
                background-color: #f1f1f1;
                border-bottom: 1px solid #ddd;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header-logo {{
                margin-right: 20px;
            }}
            .header-message {{
                font-size: 24px;
                font-weight: bold;
                color: {text_color};
                text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.5);
            }}
            .chat-container {{
                display: flex;
                flex-direction: column;
                height: 80vh;
                border: 1px solid #ddd;
                background-color: #f9f9f9;
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
            }}
            .chat-message {{
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
                transition: background-color 0.2s, transform 0.2s;
            }}
            .chat-message.user {{
                align-self: flex-end;
                background-color: #e1ffc7; /* Light green for user */
                color: #000;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
            .chat-message.bot {{
                align-self: flex-start;
                background-color: #d9edf7; /* Light blue for bot */
                color: #000;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }}
            .input-container {{
                padding: 10px;
                background-color: {input_bg_color};
                border-top: 1px solid #ddd;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                z-index: 1;
                display: flex;
                flex-direction: column;
            }}
            .input-container input {{
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                width: 100%;
                background-color: {input_bg_color};
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
                flex: 1;
                background-color: {button_color};
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
            @media (max-width: 600px) {{
                .header-message {{
                    font-size: 20px;
                }}
                .input-container input {{
                    font-size: 14px;
                }}
                .chat-message {{
                    font-size: 14px;
                }}
            }}
            /* Custom scrollbar styles */
            ::-webkit-scrollbar {{
                width: 10px;
            }}
            ::-webkit-scrollbar-track {{
                background: #f1f1f1;
            }}
            ::-webkit-scrollbar-thumb {{
                background: #888;
                border-radius: 5px;
            }}
            ::-webkit-scrollbar-thumb:hover {{
                background: #555;
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

    # Display conversation history in the chat history container
    with chat_history_container:
        chat_history = ""
        for line in reversed(st.session_state.conversation_history):
            if line.startswith("You:"):
                chat_history += f'<div class="chat-message user">{line}</div>'
            else:
                chat_history += f'<div class="chat-message bot">{line}</div>'
        st.markdown(f'<div class="chat-history">{chat_history}</div>', unsafe_allow_html=True)

    # Feedback section
    if st.sidebar.radio("Select an option:", ["Home", "Feedback", "About"]) == "Feedback":
        st.header("Feedback")
        st.write("We value your feedback! Please let us know your thoughts about the chatbot.")
        
        feedback = st.text_area("Your Feedback:", "")
        
        if st.button("Generate Feedback Link"):
            if feedback:
                feedback_link = f"mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body={feedback}"
            else:
                st.error("Please enter your feedback before sending.")
        
        if feedback:
            st.markdown(f'<a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>', unsafe_allow_html=True)

    # Updated About section
    elif st.sidebar.radio("Select an option:", ["Home", "Feedback", "About"]) == "About":
        st.header("About")
        st.write("""
        Welcome to our chatbot! This virtual friend is here to provide support for your mental health. 
        You can share your thoughts and feelings in a safe and non-judgmental environment. 
        Our aim is to listen and offer guidance to help you navigate life's challenges.
        """)

if __name__ == "__main__":
    main()
