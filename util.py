import streamlit as st
import numpy as np

def agregar_resultados_finais():
    st.subheader("\U0001F3C1 Resultado Final Agregado")

    pesos_criterios = st.session_state.get("pesos_criterios", [])
    nomes_criterios = st.session_state.get("nomes_criterios", [])
    scores_por_criterio = st.session_state.get("scores_por_criterio", {})

    if len(pesos_criterios) == 0 or len(scores_por_criterio) == 0:
        st.warning("⚠️ Não há dados suficientes para calcular o resultado final.")
        return

    alternativas = [
        "Nova York (EUA)",
        "Orlando (Disney - EUA)",
        "Paris (França)",
        "Londres (Reino Unido)",
        "Roma (Itália)",
        "Tóquio (Japão)"
    ]

    n_alt = len(alternativas)
    scores_finais = np.zeros(n_alt)

    for i, criterio in enumerate(nomes_criterios):
        if criterio in scores_por_criterio:
            scores_finais += pesos_criterios[i] * scores_por_criterio[criterio]

    for i, score in enumerate(scores_finais):
        st.write(f"{alternativas[i]}: {score:.4f}")

    melhor = alternativas[np.argmax(scores_finais)]
    st.success(f"\U0001F3C6 Melhor destino para viagem: **{melhor}**")
