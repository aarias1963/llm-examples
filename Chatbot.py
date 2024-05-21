import os
import streamlit as st
from groq import Client as GroqClient

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", key="chatbot_api_key", type="password")
    max_tokens = st.sidebar.slider(
        "Tokens máximos:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=8192,
        # Default value or max allowed if less
        value=min(32768, 8192),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: 8192"
    )
    st.button("Reiniciar chat", on_click=st.session_state.clear, args=())

st.title("💬 Chatbot")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "¡Hola! ¿En qué puedo ayudarte?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not groq_api_key:
        st.info("Por favor, introduce tu Groq API Key.")
        st.stop()

    os.environ["GROQ_API_KEY"] = groq_api_key
    client = GroqClient()
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Crear una lista de mensajes para pasar al modelo
    messages = [{"role": "assistant", "content": msg["content"]} for msg in st.session_state.messages]

    chat_completion = client.chat.completions.create(
        messages=messages + [
            {
                "role": "user",
                "content": prompt,
            },
            {"role": "system", "content": "Eres un experto asistente."}
        ],
        model="llama3-70b-8192",
        max_tokens=max_tokens
    )
    msg = chat_completion.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
