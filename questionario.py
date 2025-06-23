import streamlit as st
import urllib.parse

def exibir_questionario():
    st.header("📝 Questionário de Avaliação")

    # Recupera os dados armazenados durante o experimento
    tempos = st.session_state.get("tempos_execucao", {})
    inconsistencias = st.session_state.get("inconsistencias", 0)
    metodo = st.session_state.get("metodo", "indefinido")

    # URL base do Google Forms (com o ?usp=pp_url)
    base_url = "https://docs.google.com/forms/d/e/1FAIpQLScDn-iexyubiO_wZ1Lqei6AT5thX88MvedT8XIvmmd_zLmvjA/viewform?usp=pp_url"

    # Mapeamento atualizado com os novos entry IDs
    params = {
        "entry.650743101": metodo,
        "entry.1285941183": tempos.get("criterios", ""),
        "entry.1231849445": tempos.get("alternativas", ""),
        "entry.1140389012": inconsistencias
    }

    # Montagem final da URL
    url_completa = base_url + "&" + urllib.parse.urlencode(params)

    # Interface para o participante
    st.success("✅ Todas as etapas foram concluídas!")
    st.markdown("Clique no botão abaixo para preencher o questionário final:")
    st.markdown(f"[Preencher o Questionário no Google Forms]({url_completa})", unsafe_allow_html=True)
