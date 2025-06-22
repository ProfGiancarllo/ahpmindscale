# app.py
import streamlit as st
import random
from criterios_tradicional import comparar_criterios_tradicional
from criterios_mindscale import comparar_criterios_mindscale
from alternativas_tradicional import comparar_alternativas_tradicional
from alternativas_mindscale import comparar_alternativas_mindscale
from questionario import exibir_questionario
from registro_tempo import resetar_tempos
from PIL import Image

st.set_page_config(page_title="AHP MindScale", layout="centered")

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

# Tela inicial com logo centralizado
if st.session_state.etapa == 0:
    st.title("🧠 AHP MindScale")
    image = Image.open("logo_mindscale.png")
    st.image(image, use_container_width=True)
    
    st.markdown("""
    Bem-vindo ao experimento de avaliação de decisão com o método AHP!
    
    Clique em **Iniciar Avaliação** para começar.
    """)
    
    if st.button("Iniciar Avaliação"):
        st.session_state.metodo = random.choice(["tradicional", "mindscale"])
        st.session_state.etapa = 1
        resetar_tempos()
        st.rerun()

elif st.session_state.etapa == 1:
    if st.session_state.metodo == "tradicional":
        comparar_criterios_tradicional()
    else:
        comparar_criterios_mindscale()

    if st.session_state.criterios_concluidos:
        st.session_state.etapa = 2
        st.rerun()

elif st.session_state.etapa == 2:
    if st.session_state.metodo == "tradicional":
        comparar_alternativas_tradicional()
    else:
        comparar_alternativas_mindscale()

    if st.session_state.alternativas_concluidas:
        st.session_state.etapa = 3
        st.rerun()

elif st.session_state.etapa == 3:
    exibir_questionario()
    st.session_state.etapa = 4

elif st.session_state.etapa == 4:
    st.success("✅ Processo finalizado.")
    if st.button("Refazer Avaliação"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
