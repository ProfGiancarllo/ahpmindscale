# registro_tempo.py
import time
import streamlit as st

def iniciar_tempo(etapa):
    if "tempos_inicio" not in st.session_state:
        st.session_state["tempos_inicio"] = {}
    st.session_state["tempos_inicio"][etapa] = time.time()

def finalizar_tempo(etapa):
    if "tempos_execucao" not in st.session_state:
        st.session_state["tempos_execucao"] = {}
    inicio = st.session_state.get("tempos_inicio", {}).get(etapa)
    if inicio:
        duracao = round(time.time() - inicio, 2)
        st.session_state["tempos_execucao"][etapa] = duracao

def resetar_tempos():
    st.session_state["tempos_inicio"] = {}
    st.session_state["tempos_execucao"] = {}
