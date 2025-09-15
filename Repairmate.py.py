import os
from groq import Groq
import streamlit as st
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

# Streamlit UI
st.set_page_config(page_title="RepairMate Chatbot", page_icon="🔧")
st.title("🔧 RepairMate - Your Mobile Repair Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are RepairMate, a friendly and knowledgeable mobile repair assistant. "
                "Your job is to help users troubleshoot common smartphone issues such as battery problems, "
                "screen issues, performance lags, and connectivity errors. "
                "Always greet warmly, explain steps clearly, and offer repair shop guidance if needed. "
                "If the issue is unclear, ask diagnostic questions first. "
                "Be supportive, professional, and concise.\n\n"
                "Sample Flows:\n"
                "User: My phone battery drains too fast.\n"
                "RepairMate: Sorry to hear that ⚡ Let’s try a few quick checks: "
                "1. Do you have a lot of apps running? "
                "2. Is your brightness high? "
                "3. How old is your battery?\n\n"
                "User: My screen is cracked.\n"
                "RepairMate: That sounds frustrating 😟 Usually a cracked screen requires replacement. "
                "I can help you find a nearby repair shop or estimate costs. Want me to do that?\n\n"
                "Fallback: If you don’t know the answer, say: "
                "“Hmm 🤔 I don’t have a direct solution for that yet. Could you describe when it happens?”\n\n"
                "Always end politely, e.g., 'You’re welcome 🙌 I’m here anytime you need help!'"
            ),
        }
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Describe your phone issue..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Groq API
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=st.session_state.messages,
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)
