from dotenv import load_dotenv
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure Gemini Pro model
genai.configure(api_key=os.getenv("AIzaSyDPfS7OjuWEBitcmjBnUTqW8UQeooZrVJs"))

# Initialize Gemini Pro model
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# Function to get Gemini response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="KRK chatbot", layout="wide")
st.header("EDUCATION CHATBOT")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Sidebar for Chat History
with st.sidebar:
    st.header("Chat History")
    # Button to clear chat history
    if st.button("Clear History"):
        st.session_state['chat_history'] = []
    
    # Display only the questions in the sidebar
    for idx, (role, text) in enumerate(st.session_state['chat_history']):
        if role == "You":  # Only display user questions
            with st.expander(f"Q: {text}"):  # Collapsible section for each question
                # Display the full chat history for this question and its answer
                for r, t in st.session_state['chat_history'][idx:idx+2]:  # Question + Answer
                    st.write(f"**{r}:** {t}")

# Main chat interface
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    # Collect the entire response from all chunks
    full_response = ""
    st.subheader("The Response is")
    for chunk in response:
        full_response += chunk.text
        st.write(chunk.text)  # Display each chunk in the main area
    
    # Add the full response to the chat history
    st.session_state['chat_history'].append(("Bot", full_response))