# criterios_tradicional.py
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo


def comparar_criterios_tradicional():
    iniciar_tempo("criterios")

    st.subheader("Etapa 1: Comparação entre Critérios (Método Tradicional)")
    st.subheader("Compare os criterios segundo a escala apresentada, não tenha pressa, siga no seu tempo")

    criterios = [
        "Custo da Viagem",
        "Belezas Naturais",
        "Atrativos Culturais",
        "Gastronomia",
        "Compras"
    ]
    n = len(criterios)

    legenda = {
        1: "a mesma importância em relação",
        2: "a importância levemente superior",
        3: "a importância pouco superior",
        4: "a importância moderadamente superior",
        5: "a importância muito superior",
        6: "a importância fortemente superior",
        7: "a importância extremamente superior",
        8: "a importância quase absolutamente superior",
        9: "a importância absolutamente superior"
    }

    matriz = [[1 if i == j else None for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            col1, col2 = st.columns([3, 2])
            with col1:
                valor = st.select_slider(
                    f"{criterios[i]} vs {criterios[j]}",
                    options=[1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9],
                    value=1,
                    format_func=lambda x: str(round(x, 3)),
                    key=f"criterio_{i}_{j}"
                )
                matriz[i][j] = valor
                matriz[j][i] = round(1 / valor, 4)
            with col2:
                if valor >= 1:
                    frase = legenda[int(valor)]
                    st.markdown(f"**{valor}** – **O critério {criterios[i]}** tem {frase} ao critério **{criterios[j]}**")
                else:
                    frase = legenda[int(round(1 / valor))]
                    st.markdown(f"**{valor}** – **O critério {criterios[j]}** tem {frase} ao critério **{criterios[i]}**")

    def calcular_pesos(matriz):
        matriz = np.array(matriz)
        soma_colunas = matriz.sum(axis=0)
        matriz_normalizada = matriz / soma_colunas
        return matriz_normalizada.mean(axis=1)

    def calcular_consistencia(matriz, pesos):
        n = len(matriz)
        matriz = np.array(matriz)
        w = np.dot(matriz, pesos)
        lambda_max = (w / pesos).mean()
        CI = (lambda_max - n) / (n - 1)
        RI_dict = {
            1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12,
            6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49
        }
        RI = RI_dict.get(n, 1.49)
        CR = CI / RI if RI != 0 else 0
        return CR

    if all(matriz[i][j] is not None for i in range(n) for j in range(n)):
        pesos = calcular_pesos(matriz)
        CR = calcular_consistencia(matriz, pesos)

        st.write(f"Razão de Consistência (CR): {CR:.4f}")
        if CR <= 0.1:
            st.success("✅ Matriz consistente")
            st.session_state["criterios_concluidos"] = True
            st.session_state["nomes_criterios"] = criterios
            st.session_state["pesos_criterios"] = pesos
            finalizar_tempo("criterios")
        else:
            st.error("❌ Matriz inconsistente. Ajuste os valores para melhorar a consistência.")
            st.session_state["inconsistencias"] += 1
    else:
        st.warning("⚠️ Preencha todos os valores da matriz antes de prosseguir.")

