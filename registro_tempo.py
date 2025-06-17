import time
import streamlit as st

def iniciar_tempo(etapa):
    chave_inicio = f"tempo_inicio_{etapa}"
    if chave_inicio not in st.session_state:
        st.session_state[chave_inicio] = time.time()

def finalizar_tempo(etapa):
    chave_inicio = f"tempo_inicio_{etapa}"
    chave_fim = f"tempo_fim_{etapa}"
    chave_total = f"tempo_total_{etapa}"
    if chave_inicio in st.session_state:
        st.session_state[chave_fim] = time.time()
        st.session_state[chave_total] = round(st.session_state[chave_fim] - st.session_state[chave_inicio], 2)
def resetar_tempos():
    chaves_tempo = [k for k in st.session_state.keys() if k.startswith("tempo_inicio_") or k.startswith("tempo_fim_")]
    for chave in chaves_tempo:
        del st.session_state[chave]

    if "inconsistencias" in st.session_state:
        st.session_state["inconsistencias"] = 0
