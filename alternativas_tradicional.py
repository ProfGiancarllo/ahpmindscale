# alternativas_tradicional.py
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo
from exibir_resultado import exibir_resultado

def comparar_alternativas_tradicional():
    iniciar_tempo("alternativas")

    if "criterios_concluidos" not in st.session_state or not st.session_state["criterios_concluidos"]:
        st.warning("Conclua a etapa de critérios primeiro.")
        return

    st.subheader("Etapa 2: Comparação entre Alternativas (Método Tradicional)")

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
                valor = st.select_slider(
                    f"{alternativas[i]} vs {alternativas[j]} ({criterio})",
                    options=[1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9],
                    value=1,
                    format_func=lambda x: str(round(x, 3)),
                    key=f"alt_{idx}_{i}_{j}"
                )
                matriz[i][j] = valor
                matriz[j][i] = round(1/valor, 4)

        matriz_np = np.array(matriz)
        soma_col = matriz_np.sum(axis=0)
        matriz_norm = matriz_np / soma_col
        pesos = matriz_norm.mean(axis=1)
        resultados[criterio] = pesos

    st.session_state["alternativas_concluidas"] = True
    finalizar_tempo("alternativas")

    # Cálculo do resultado final
    final_scores = np.zeros(len(alternativas))
    for idx, criterio in enumerate(criterios):
        final_scores += np.array(resultados[criterio]) * pesos_criterios[idx]

    exibir_resultado(final_scores, alternativas)
