# app.py
import streamlit as st
import random
from criterios_tradicional import comparar_criterios_tradicional
from criterios_mindscale import comparar_criterios_mindscale
from alternativas_tradicional import comparar_alternativas_tradicional
from alternativas_mindscale import comparar_alternativas_mindscale
from questionario import exibir_questionario
from registro_tempo import resetar_tempos

st.set_page_config(page_title="AHP MindScale", layout="wide")

if "etapa" not in st.session_state:
    st.session_state.etapa = 0
if "metodo" not in st.session_state:
    st.session_state.metodo = None
if "criterios_concluidos" not in st.session_state:
    st.session_state.criterios_concluidos = False
if "alternativas_concluidas" not in st.session_state:
    st.session_state.alternativas_concluidas = False
if "inconsistencias" not in st.session_state:
    st.session_state.inconsistencias = 0
if "tempos_execucao" not in st.session_state:
    st.session_state["tempos_execucao"] = {}

if st.session_state.etapa == 0:
    st.image("logo_inicial.png", use_column_width=True)
    st.title("Bem-vindo ao AHP MindScale")

    st.markdown("""
    Este aplicativo faz parte de uma pesquisa de doutorado.
    
    Você fará uma série de comparações e ao final responderá um pequeno questionário.
    
    Ao clicar em **Iniciar**, o sistema irá sortear automaticamente qual método será aplicado.
    """)
    if st.button("Iniciar"):
        st.session_state.metodo = random.choice(["Tradicional", "MindScale"])
        resetar_tempos()
        st.session_state.etapa = 1
        st.rerun()

elif st.session_state.etapa == 1:
    st.header(f"Etapa 1: Comparação de Critérios ({st.session_state.metodo})")
    if st.session_state.metodo == "Tradicional":
        comparar_criterios_tradicional()
    else:
        comparar_criterios_mindscale()

    if st.session_state.criterios_concluidos:
        if st.button("Seguir para Comparação de Alternativas"):
            st.session_state.etapa = 2
            st.rerun()

elif st.session_state.etapa == 2:
    st.header(f"Etapa 2: Comparação de Alternativas ({st.session_state.metodo})")
    if st.session_state.metodo == "Tradicional":
        comparar_alternativas_tradicional()
    else:
        comparar_alternativas_mindscale()

    if st.session_state.alternativas_concluidas:
        if st.button("Seguir para Questionário"):
            st.session_state.etapa = 3
            st.rerun()

elif st.session_state.etapa == 3:
    exibir_questionario()
