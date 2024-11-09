import streamlit as st
from pages import page1, page2

st.set_page_config(page_title="Mi Aplicación Appp Streamlit", layout="wide")

# Crear un menú de navegación
menu = ["Página 1", "Página 2"]
choice = st.sidebar.selectbox("Selecciona una página", menu)

if choice == "Página 1":
    page1.app()
elif choice == "Página 2":
    page2.app()
