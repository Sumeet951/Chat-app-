import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

if "message" not in st.session_state:
    st.session_state.message = []

for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here")

if user_input:
    st.session_state.message.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=list(
            map(lambda message: message["role"] + ":" + message["content"],
                st.session_state.message)
        )
    )

    # 👇 MOVE THIS INSIDE THE IF BLOCK
    st.session_state.message.append({
        "role": "assistant",   # change from "ai" to "assistant"
        "content": response.text
    })

    with st.chat_message("assistant"):
        st.markdown(response.text)