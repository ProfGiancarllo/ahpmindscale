# criterios_mindscale.py
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo

def comparar_criterios_mindscale():
    iniciar_tempo("criterios")

    st.subheader("Etapa 1: Comparação entre Critérios (MindScale)")
    st.subheader("Compare os criterios segundo a escala apresentada, não tenha pressa, siga no seu tempo")

    criterios = [
        "Custo da Viagem",
        "Belezas Naturais",
        "Atrativos Culturais",
        "Gastronomia",
        "Compras"
    ]
    n = len(criterios)

    valores_mindscale = list(range(1, 10))
    legenda = {
        1: "têm igual importância",
        2: "é levemente mais importante que",
        3: "é um pouco mais importante que",
        4: "é moderadamente mais importante que",
        5: "é fortemente mais importante que",
        6: "é muito mais importante que",
        7: "é muito mais importante que (quase extremo)",
        8: "é extremamente mais importante que",
        9: "é absolutamente mais importante que"
    }

    base = st.selectbox("Na sua opinião, considerando todos os critérios, qual é o mais importante?", criterios)
    base_index = criterios.index(base)

    st.markdown("### Compare os demais critérios em relação ao critério mais importante (referência)")

    comparacoes = {}

    for i in range(n):
        if i != base_index:
            col1, col2 = st.columns([3, 2])
            with col1:
                valor = st.slider(f"{criterios[i]} vs {base}", min_value=1, max_value=9, value=5, key=f"comp_{i}")
                comparacoes[(i, base_index)] = round(1 / valor, 4)
                comparacoes[(base_index, i)] = valor
            with col2:
                frase = legenda[valor]
                st.markdown(f"**{valor}** – **{base}** {frase} **{criterios[i]}**")

    matriz = [[1.0 if i == j else None for j in range(n)] for i in range(n)]

    for (i, j), v in comparacoes.items():
        matriz[i][j] = v

    for i in range(n):
        for j in range(n):
            if matriz[i][j] is None and matriz[i][base_index] is not None and matriz[base_index][j] is not None:
                matriz[i][j] = round(matriz[i][base_index] * matriz[base_index][j], 4)

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

        st.subheader("Pesos dos Critérios")
        for i, peso in enumerate(pesos):
            st.write(f"{criterios[i]}: {peso:.4f}")

        st.write(f"Razão de Consistência (CR): {CR:.4f}")
        if CR <= 0.1:
            st.success("✅ A matriz é consistente (CR ≤ 0.1)")
            st.session_state["criterios_concluidos"] = True
            st.session_state["pesos_criterios"] = pesos
            st.session_state["nomes_criterios"] = criterios
            finalizar_tempo("criterios")
        else:
            st.error("❌ A matriz é inconsistente (CR > 0.1). Ajuste os valores para melhorar a consistência.")
            st.session_state["inconsistencias"] += 1
    else:
        st.warning("⚠️ Preencha todos os valores da matriz antes de prosseguir.")

   