# app.py

import streamlit as st
import requests

# Configurar las claves desde los secrets
API_FOOTBALL_API_KEY = st.secrets["API_FOOTBALL_API_KEY"]
XAI_API_KEY = st.secrets["XAI_API_KEY"]

# Título de la aplicación
st.title("Chatbot de Predicción de la Champions League")

# Barra lateral para selección de equipos
st.sidebar.header("Selecciona los Equipos")

# ID de la UEFA Champions League obtenido previamente
LEAGUE_ID = 2790  # Reemplaza con el ID correcto obtenido
SEASON = 2023  # Ajusta según sea necesario

# Función para obtener la lista de equipos
def get_teams(league_id, season=SEASON):
    url = "https://v3.football.api-sports.io/teams"
    headers = {
        "x-apisports-key": API_FOOTBALL_API_KEY
    }
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        teams = [team["team"]["name"] for team in data["response"]]
        return teams
    else:
        st.error(f"Error al obtener los equipos: {response.status_code} - {response.text}")
        return []

# Obtener la lista de equipos
teams = get_teams(LEAGUE_ID, SEASON)

if not teams:
    st.stop()

# Selección de equipos
equipo_local = st.sidebar.selectbox("Equipo Local", teams)
equipo_visitante = st.sidebar.selectbox("Equipo Visitante", teams)

# Área de chat
st.header("Chatbot de Predicción")

# Entrada del usuario
user_input = st.text_input("Tú:", "Predice el resultado del partido.")

if st.button("Enviar"):
    if user_input:
        # Función para obtener estadísticas de los equipos
        def get_team_stats(team_name, league_id, season=SEASON):
            url = "https://v3.football.api-sports.io/teams/statistics"
            headers = {
                "x-apisports-key": API_FOOTBALL_API_KEY
            }
            params = {
                "team": team_name,
                "league": league_id,
                "season": season
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error al obtener estadísticas para {team_name}: {response.status_code} - {response.text}")
                return None

        stats_local = get_team_stats(equipo_local, LEAGUE_ID, SEASON)
        stats_visitante = get_team_stats(equipo_visitante, LEAGUE_ID, SEASON)

        if stats_local and stats_visitante:
            # Preparar el prompt para X AI
            prompt = (
                f"Basándote en las siguientes estadísticas, predice el resultado del partido entre "
                f"{equipo_local} y {equipo_visitante}.\n\n"
                f"Estadísticas {equipo_local}: {stats_local}\n\n"
                f"Estadísticas {equipo_visitante}: {stats_visitante}\n\n"
                f"Predicción:"
            )

            # Configurar la solicitud a X AI
            xai_url = "https://api.x.ai/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {XAI_API_KEY}"
            }
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a sports prediction assistant specialized in Champions League matches."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "model": "grok-beta",
                "stream": False,
                "temperature": 0.7
            }

            try:
                response = requests.post(xai_url, headers=headers, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    # Asumiendo que la respuesta de X AI tiene una estructura similar a OpenAI
                    prediction = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                    st.text_area("Predicción del Chatbot:", prediction, height=200)
                else:
                    st.error(f"Error en la API de X AI: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error al obtener la predicción: {e}")
        else:
            st.error("No se pudieron obtener las estadísticas de los equipos.")
    else:
        st.warning("Por favor, ingresa una consulta.")
