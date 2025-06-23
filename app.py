# app.py

import streamlit as st
import random
from criterios_tradicional import comparar_criterios_tradicional
from criterios_mindscale import comparar_criterios_mindscale
from alternativas_tradicional import comparar_alternativas_tradicional
from alternativas_mindscale import comparar_alternativas_mindscale
from questionario import exibir_questionario
from registro_tempo import resetar_tempos

st.set_page_config(page_title="AHP MindScale", layout="centered")

# Inicializar variáveis de estado
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

# Etapa 0 - Boas vindas
if st.session_state.etapa == 0:
    st.image("logo.png", width=300)  # (coloque seu arquivo logo.png no repositório)
    st.title("Bem-vindo ao Sistema de Apoio à Decisão de Viagem")

    st.markdown("""
    Este aplicativo faz parte de uma pesquisa de doutorado e visa comparar métodos de decisão multicritério.

    Você será guiado(a) por algumas etapas:
    - Comparação de critérios
    - Comparação de alternativas
    - Avaliação final (questionário)

    Clique em **Iniciar Avaliação** quando estiver pronto(a).
    """)
    if st.button("Iniciar Avaliação"):
        st.session_state.metodo = random.choice(["tradicional", "mindscale"])
        st.session_state.etapa = 1
        resetar_tempos()
        st.rerun()

# Etapa 1 - Comparação de Critérios
elif st.session_state.etapa == 1:
    st.info(f"🧪 Método Sorteado: **{'AHP Tradicional' if st.session_state.metodo == 'tradicional' else 'AHP MindScale'}**")
    if st.session_state.metodo == "tradicional":
        comparar_criterios_tradicional()
    else:
        comparar_criterios_mindscale()

    if st.session_state.criterios_concluidos:
        if st.button("Seguir para a próxima etapa"):
            st.session_state.etapa = 2
            st.rerun()

# Etapa 2 - Comparação de Alternativas
elif st.session_state.etapa == 2:
    st.info(f"🧪 Método Sorteado: **{'AHP Tradicional' if st.session_state.metodo == 'tradicional' else 'AHP MindScale'}**")
    if st.session_state.metodo == "tradicional":
        comparar_alternativas_tradicional()
    else:
        comparar_alternativas_mindscale()

    if st.session_state.alternativas_concluidas:
        if st.button("Seguir para a próxima etapa"):
            st.session_state.etapa = 3
            st.rerun()

# Etapa 3 - Questionário Final
elif st.session_state.etapa == 3:
    exibir_questionario()
    st.session_state.etapa = 4

# Etapa 4 - Encerramento
elif st.session_state.etapa == 4:
    st.success("✅ Avaliação concluída com sucesso. Muito obrigado!")
    if st.button("Refazer Avaliação"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
