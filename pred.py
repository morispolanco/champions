# app.py

import streamlit as st
import requests

# Configurar las claves desde los secrets
API_FOOTBALL_API_KEY = st.secrets["API_FOOTBALL_API_KEY"]
XAI_API_KEY = st.secrets["XAI_API_KEY"]

# Título de la aplicación
st.title("Depuración y Configuración de la Champions League en API-Football")

# Temporada
SEASON = 2023  # Ajusta según sea necesario

# Función para listar todas las ligas disponibles
def listar_todas_ligas(temporada=SEASON):
    url = "https://v3.football.api-sports.io/leagues"
    headers = {
        "x-apisports-key": API_FOOTBALL_API_KEY
    }
    params = {
        "season": temporada
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        ligas = data.get("response", [])
        st.subheader(f"Todas las Ligas Disponibles para la Temporada {temporada}:")
        for liga in ligas:
            nombre_liga = liga["league"]["name"]
            id_liga = liga["league"]["id"]
            pais = liga["country"]["name"]
            st.write(f"- **{nombre_liga}** (ID: {id_liga}) - País: {pais}")
    else:
        st.error(f"Error al obtener las ligas: {response.status_code} - {response.text}")

# Función para buscar ligas por palabra clave
def buscar_ligas_por_palabra_clave(palabra_clave="Champions", temporada=SEASON):
    url = "https://v3.football.api-sports.io/leagues"
    headers = {
        "x-apisports-key": API_FOOTBALL_API_KEY
    }
    params = {
        "search": palabra_clave,
        "season": temporada
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["response"]
    else:
        st.error(f"Error al obtener las ligas: {response.status_code} - {response.text}")
        return []

# Función para listar ligas por país
def listar_ligas_por_pais(pais="Europe", temporada=SEASON):
    url = "https://v3.football.api-sports.io/leagues"
    headers = {
        "x-apisports-key": API_FOOTball_API_KEY
    }
    params = {
        "season": temporada
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        ligas = data.get("response", [])
        st.subheader(f"Ligas en {pais} para la Temporada {temporada}:")
        for liga in ligas:
            nombre_liga = liga["league"]["name"]
            id_liga = liga["league"]["id"]
            liga_pais = liga["country"]["name"]
            if liga_pais.lower() == pais.lower():
                st.write(f"- **{nombre_liga}** (ID: {id_liga})")
    else:
        st.error(f"Error al obtener las ligas: {response.status_code} - {response.text}")

# Opciones de depuración
st.sidebar.header("Opciones de Depuración")
opcion = st.sidebar.selectbox(
    "Selecciona una opción para depurar:",
    ("Listar Todas las Ligas", "Buscar Ligas por Palabra Clave", "Listar Ligas por País")
)

if opcion == "Listar Todas las Ligas":
    listar_todas_ligas()
elif opcion == "Buscar Ligas por Palabra Clave":
    palabra_clave = st.text_input("Ingrese una palabra clave para buscar ligas:", "Champions")
    if st.button("Buscar"):
        ligas_encontradas = buscar_ligas_por_palabra_clave(palabra_clave=palabra_clave)
        if ligas_encontradas:
            st.subheader(f"Ligas Encontradas con la Palabra Clave '{palabra_clave}':")
            for liga in ligas_encontradas:
                nombre_liga = liga["league"]["name"]
                id_liga = liga["league"]["id"]
                pais = liga["country"]["name"]
                st.write(f"- **{nombre_liga}** (ID: {id_liga}) - País: {pais}")
        else:
            st.error("No se encontraron ligas que coincidan con la búsqueda de la palabra clave.")
elif opcion == "Listar Ligas por País":
    pais = st.text_input("Ingrese el nombre del país para listar ligas:", "Europe")
    if st.button("Listar"):
        listar_ligas_por_pais(pais=pais)

st.stop()  # Detener la ejecución aquí para evitar errores adicionales
