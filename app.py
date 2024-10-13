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
# Split the string by commas and remove any extra whitespace
api_keys_list = [key.strip() for key in api_keys_string.split(',') if key.strip()]

# Select a random API key from the list
random_api_key = random.choice(api_keys_list)

    # Create prompt with the full conversation history
    conversation_history = "\n".join(st.session_state.conversation_history)
    prompt = chat_prompt.format(conversation_history=conversation_history)
    
    try:
        prompt = chat_prompt.format(conversation_history=conversation_history)
        # Invoke Llama model via Groq API
        response = llm.invoke(prompt)
        chatbot_response = response.content.strip() if hasattr(response, 'content') else "Sorry, I didn't get that."

    if menu_option == "Home":
        # Chatbot interface
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
        st.write("""
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
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 80vh;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
            border-radius: 8px;
            overflow: hidden;
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
            border-radius: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .chat-message.user {
            align-self: flex-end;
            background-color: #e1ffc7; /* Light green for user */
            color: #000;
        }
        .chat-message.bot {
            align-self: flex-start;
            background-color: #d9edf7; /* Light blue for bot */
            color: #000;
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
            width: 100%;
        }
        .input-container button {
            padding: 15px;  /* Increased size */
            border: none;
            border-radius: 8px;
            font-size: 18px;  /* Increased font size */
            font-weight: bold;
            color: white !important;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            flex: 1;
            position: relative;  /* For animation */
            overflow: hidden;  /* For button effect */
        }
        .input-container button.send-button {
            background-color: #87CEEB !important;
        }
        .input-container button.send-button:hover {
            background-color: #00BFFF !important;
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        .input-container button.restart-button {
            background-color: #28a745 !important;
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
        @media (max-width: 600px) {
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
                border-radius: 8px;
                overflow: hidden;
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
                border-radius: 10px;
                max-width: 80%;
                word-wrap: break-word;
            }
            .chat-message.user {
                align-self: flex-end;
                background-color: #e1ffc7; /* Light green for user */
                color: #000;
            }
            .chat-message.bot {
                align-self: flex-start;
                background-color: #d9edf7; /* Light blue for bot */
                color: #000;
            }
            .input-container {
                padding: 10px;
                background-color: #fff;
                border-top: 1px solid #ddd;
                box-shadow: 0 -1px 5px rgba(0,0,0,0.1);
                z-index: 1;
                display: flex;
                flex-direction: column;
                font-size: 20px;
            }
            .input-container input {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-bottom: 10px;
                width: 100%;
            }
            .input-container button {
                padding: 15px;  /* Increased size */
                border: none;
                border-radius: 8px;
                font-size: 18px;  /* Increased font size */
                font-weight: bold;
                color: white !important;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                flex: 1;
                position: relative;  /* For animation */
                overflow: hidden;  /* For button effect */
            }
            .input-container button.send-button {
                background-color: #87CEEB !important;
            }
            .input-container button.send-button:hover {
                background-color: #00BFFF !important;
                transform: scale(1.05);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }
            .input-container button.restart-button {
                background-color: #28a745 !important;
                font-size: 14px;
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
            .chat-message {
                font-size: 14px;
            }
            </style>
            """, unsafe_allow_html=True
        }
        </style>
        """, unsafe_allow_html=True
        )

        st.markdown("""<div class="header-container">
        if st.button("Generate Feedback Link"):
            if feedback:
                feedback_link = f"mailto:khashedofficial@gmail.com?subject=Feedback on Chatbot&body={feedback}"
                st.markdown(f'<a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>', unsafe_allow_html=True)
            else:
                st.error("Please enter your feedback before sending.")
        
        if feedback:
            st.markdown(f'<a href="{feedback_link}" class="feedback-button">📧 Send Feedback via Email</a>', unsafe_allow_html=True)

    elif menu_option == "About":
        # Updated About section
        st.header("About")
        st.write("""
        st.write(""" 
        Welcome to our chatbot! This virtual friend is here to provide support for your mental health. 
        You can share your thoughts and feelings in a safe and non-judgmental environment. 
        Our aim is to listen and offer guidance to help you navigate life's challenges.
        """)

if __name__ == "__main__":
    main()
