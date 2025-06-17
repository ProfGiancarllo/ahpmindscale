import random
import streamlit as st

def sortear_metodo():
    if "metodo_escolhido" not in st.session_state:
        opcoes = ["AHP Tradicional", "AHP MindScale"]
        escolhido = random.choice(opcoes)
        st.session_state["metodo_escolhido"] = escolhido
        st.success(f"Método sorteado: {escolhido}")
    return st.session_state["metodo_escolhido"]
