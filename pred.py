import streamlit as st
import requests
import json

# Cargar la API Key desde los secrets de Streamlit
api_key = st.secrets["XAI_API_KEY"]

# Definir la función para obtener la respuesta del chatbot
def get_chatbot_response():
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a writer assistant."},
            {"role": "user", "content": "Testing. Just say hi and hello world and nothing else."}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Crear la interfaz de usuario en Streamlit
st.title("Chatbot de Streamlit con x.ai")
if st.button("Enviar mensaje"):
    response = get_chatbot_response()
    st.write(response)

# Para esconder la API Key, añade lo siguiente en el archivo .streamlit/secrets.toml
# [XAI_API_KEY]
# api_key = "tu_api_key_aqui"
