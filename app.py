import os
import random
import streamlit as st
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# Get the API keys as a single string from the environment variable
api_keys_string = os.getenv('GROQ_API_KEYS')

# Split the string by newlines and remove any extra whitespace
        st.session_state.conversation_history.append(f"Chatbot: Error occurred: {str(e)}")

def main():
    st.set_page_config(page_title="Chatbot", layout="wide")  # Set wide mode
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
    # Sidebar for navigation with dynamic styles
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Select an option:", ["Home", "Feedback", "About"])
    menu_option = st.sidebar.radio("Select an option:", ["Home", "Feedback", "About"], 
                                     index=0, key="menu")
    # Apply dynamic styles to the sidebar
    st.markdown("""
        <style>
            .stRadio > label {
                display: block;
                padding: 10px;
                margin: 5px 0;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            .stRadio > label:hover {
                background-color: #e0f7fa;  /* Light cyan on hover */
            }
            .stRadio > div {
                margin-bottom: 15px;
            }
        </style>
    """, unsafe_allow_html=True)

    if menu_option == "Home":
        # Chatbot interface
        st.header("Feedback")
        st.write("We value your feedback! Please let us know your thoughts about the chatbot.")

        # Get user feedback
        feedback = st.text_area("Your Feedback:", "")

        # Button to generate mailto link
        if st.button("Generate Feedback Link"):
            if feedback:
                feedback_link = f"mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body={feedback}"
                #st.markdown(f"Thank you for your feedback! You can send it [here]({feedback_link}).")
            else:
                st.error("Please enter your feedback before sending.")

        # Feedback button outside the form (optional)
        if feedback:
            st.markdown(f"""
            <a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>
            """, unsafe_allow_html=True)
            st.markdown(f'<a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>', unsafe_allow_html=True)

    elif menu_option == "About":
        # About section
        # Updated About section
        st.header("About")
        st.write("""
        This is a model chatbot designed for mental health support. 
        It provides advice as a psychiatric friend and offers a non-judgmental listening ear. 
        Feel free to share your thoughts and emotions; we're here to help!
        Welcome to our chatbot! This virtual friend is here to provide support for your mental health. 
        You can share your thoughts and feelings in a safe and non-judgmental environment. 
        Our aim is to listen and offer guidance to help you navigate life's challenges.
        """)

if __name__ == "__main__":
