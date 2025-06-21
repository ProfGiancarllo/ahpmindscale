import streamlit as st
import urllib.parse

def exibir_questionario():
    st.header("📝 Questionário de Avaliação")

    # Recupera os dados armazenados durante o experimento
    tempos = st.session_state.get("tempos_execucao", {})
    inconsistencias = st.session_state.get("inconsistencias", 0)
    metodo = st.session_state.get("metodo", "indefinido")

    # URL base do Google Forms
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLScDn-iexyubiO_wZ1Lqei6AT5thX88MvedT8XIvmmd_zLmvjA/viewform?usp=pp_url"

    # Mapeamento dos parâmetros para os entry IDs do Google Forms
    params = {
        "entry.1104627828": metodo,
        "entry.494086378": tempos.get("criterios", ""),
        "entry.1572871620": tempos.get("alternativas", ""),
        "entry.670818171": inconsistencias
    }

    # Montagem final da URL com os parâmetros codificados
    url_completa = base_url + "&" + urllib.parse.urlencode(params)

    # Interface final para o participante
    st.success("✅ Todas as etapas foram concluídas!")
    st.markdown("Clique no botão abaixo para preencher o questionário final:")
    st.markdown(f"[Preencher o Questionário no Google Forms]({url_completa})", unsafe_allow_html=True)

