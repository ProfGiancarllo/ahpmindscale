import streamlit as st
import numpy as np
import urllib.parse

def exibir_resultado():
    alternativas = [
        "Nova York (EUA)",
        "Orlando (Disney - EUA)",
        "Paris (França)",
        "Londres (Reino Unido)",
        "Roma (Itália)",
        "Tóquio (Japão)"
    ]

    criterios = st.session_state["nomes_criterios"]
    pesos_criterios = st.session_state["pesos_criterios"]
    resultados_alternativas = st.session_state["resultados_alternativas"]

    st.subheader("Resultado Final")

    n_alt = len(alternativas)
    scores_finais = np.zeros(n_alt)

    for idx, criterio in enumerate(criterios):
        scores_finais += np.array(resultados_alternativas[criterio]) * pesos_criterios[idx]

    for i, score in enumerate(scores_finais):
        st.write(f"{alternativas[i]}: {score:.4f}")

    melhor = alternativas[np.argmax(scores_finais)]
    st.markdown(
        f"<h1 style='text-align: center; color: green; font-size: 40px;'>🏆 Melhor destino: {melhor}</h1>",
        unsafe_allow_html=True
    )

    # AGORA AQUI COMEÇA O ENVIO DOS DADOS PARA O GOOGLE FORMS
    st.subheader("Envio de Dados da Pesquisa")

    # IDs dos campos do Google Forms (os entry.xxxxx que você coletou)
    entry_metodo = "entry.1104627828"
    entry_criterios = "entry.494086378"
    entry_alternativas = "entry.1780294763"
    entry_inconsistencias = "entry.1140431123"

    parametros = {
        entry_metodo: st.session_state.get("metodo", ""),
        entry_criterios: st.session_state.get("tempo_criterios", ""),
        entry_alternativas: st.session_state.get("tempo_alternativas", ""),
        entry_inconsistencias: st.session_state.get("inconsistencias", ""),
    }

    params_codificados = urllib.parse.urlencode(parametros)

    google_form_id = "1FAIpQLScDn-iexyubiO_wZ1Lqei6AT5thX88MvedT8XIvmmd_zLmvjA"
    url_forms = f"https://docs.google.com/forms/d/e/{google_form_id}/viewform?{params_codificados}"

    if st.button("Enviar dados para a pesquisa"):
        st.markdown(f"[Clique aqui para enviar suas respostas ao Google Forms]({url_forms})", unsafe_allow_html=True)
