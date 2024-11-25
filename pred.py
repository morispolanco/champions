import streamlit as st
import requests

# Cargar claves API desde los secrets
api_football_key = st.secrets["api_football_key"]
xai_api_key = st.secrets["xai_api_key"]

def predict_match_winner(home_team, away_team):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    headers = {
        "x-rapidapi-key": api_football_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    params = {"home_team": home_team, "away_team": away_team}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200 and 'response' in data and data['response']:
        prediction = data['response'][0]['predictions']['winner']
        return prediction['name'] if prediction else "No winner predicted."
    else:
        st.error(f"Error: {data.get('message', 'No prediction available.')}")
        return "Prediction not available."

def ask_xai(prompt):
    url = "https://api.x.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {xai_api_key}"
    }
    data = {
        "messages": [
            {"role": "system", "content": "You are a writer assistant."},
            {"role": "user", "content": prompt}
        ],
        "model": "grok-beta",
        "stream": False,
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

st.title("Predicción de Resultados de la Champions League")
st.write("Usa la API de API-Football para predecir el ganador de un partido.")

home_team = st.text_input("Equipo local")
away_team = st.text_input("Equipo visitante")

if st.button("Predecir"):
    prediction = predict_match_winner(home_team, away_team)
    st.write(f"Predicción: {prediction}")

st.write("También puedes hacer preguntas a X.AI:")
prompt = st.text_input("Pregunta a X.AI")

if st.button("Preguntar"):
    response = ask_xai(prompt)
    st.write(f"X.AI: {response}")
