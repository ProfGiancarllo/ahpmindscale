# alternativas_mindscale.py
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo
from exibir_resultado import exibir_resultado

def comparar_alternativas_mindscale():
    iniciar_tempo("alternativas")

    if "criterios_concluidos" not in st.session_state or not st.session_state["criterios_concluidos"]:
        st.warning("Conclua a etapa de critérios primeiro.")
        return

    st.subheader("Etapa 2: Comparação MindScale")

    alternativas = [
        "Nova York", "Orlando (Disney)", "Paris", "Londres", "Roma", "Tóquio"
    ]
    criterios = st.session_state["nomes_criterios"]
    pesos_criterios = st.session_state["pesos_criterios"]

    resultados = {}

    for idx, criterio in enumerate(criterios):
        st.markdown(f"### Critério: {criterio}")
        matriz = [[1 if i == j else None for j in range(len(alternativas))] for i in range(len(alternativas))]

        for i in range(len(alternativas)):
            for j in range(i+1, len(alternativas)):
                col1, col2 = st.columns(2)
                with col1:
                    preferido = st.radio(
                        f"Entre {alternativas[i]} e {alternativas[j]} ({criterio}), qual você prefere?",
                        [alternativas[i], alternativas[j]],
                        key=f"pref_{idx}_{i}_{j}"
                    )
                with col2:
                    if preferido == alternativas[i]:
                        valor = st.slider("Nível de certeza", 1, 9, 5, key=f"nivel_{idx}_{i}_{j}")
                        matriz[i][j] = valor
                        matriz[j][i] = round(1/valor, 4)
                    else:
                        valor = st.slider("Nível de certeza", 1, 9, 5, key=f"nivel_{idx}_{j}_{i}")
                        matriz[j][i] = valor
                        matriz[i][j] = round(1/valor, 4)

        matriz_np = np.array(matriz)
        soma_col = matriz_np.sum(axis=0)
        matriz_norm = matriz_np / soma_col
        pesos = matriz_norm.mean(axis=1)
        resultados[criterio] = pesos

    st.session_state["alternativas_concluidas"] = True
    finalizar_tempo("alternativas")

    final_scores = np.zeros(len(alternativas))
    for idx, criterio in enumerate(criterios):
        final_scores += np.array(resultados[criterio]) * pesos_criterios[idx]

    exibir_resultado(final_scores, alternativas)
