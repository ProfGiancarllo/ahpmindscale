import streamlit as st
import time

# Frases de apoio da escala
legenda = {
    1: "igual importância",
    3: "moderadamente mais importante",
    5: "fortemente mais importante",
    7: "muito fortemente mais importante",
    9: "extremamente mais importante"
}

def comparar_alternativas_tradicional(alternativas, criterio):
    if "tempo_inicio_alternativas" not in st.session_state:
        st.session_state["tempo_inicio_alternativas"] = time.time()

    n = len(alternativas)
    matriz = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    st.header(f"Comparação das Alternativas - Critério: {criterio}")

    for i in range(n):
        for j in range(i + 1, n):
            st.markdown("---")
            st.subheader(f"Comparação entre: **{alternativas[i]}** vs **{alternativas[j]}**")

            # Primeiro: escolha quem é melhor
            escolha = st.radio(
                "Qual alternativa você considera melhor?",
                (alternativas[i], alternativas[j]),
                horizontal=True,
                key=f"escolha_{i}_{j}"
            )

            # Segundo: definir intensidade
            if escolha == alternativas[i]:
                faixa = [1, 3, 5, 7, 9]
                valor = st.slider(
                    f"Quão mais importante é {alternativas[i]} em relação a {alternativas[j]}?",
                    min_value=1, max_value=9, step=2, value=1,
                    key=f"slider_{i}_{j}"
                )
                matriz[i][j] = valor
                matriz[j][i] = round(1 / valor, 4)
                frase = legenda[valor]
                st.info(f"Você indicou que **{alternativas[i]}** é **{frase}** do que **{alternativas[j]}**.")
            else:
                faixa = [1, 3, 5, 7, 9]
                valor = st.slider(
                    f"Quão mais importante é {alternativas[j]} em relação a {alternativas[i]}?",
                    min_value=1, max_value=9, step=2, value=1,
                    key=f"slider_{j}_{i}"
                )
                matriz[j][i] = valor
                matriz[i][j] = round(1 / valor, 4)
                frase = legenda[valor]
                st.info(f"Você indicou que **{alternativas[j]}** é **{frase}** do que **{alternativas[i]}**.")

    # Salvar tempo de execução
    tempo_final = time.time() - st.session_state["tempo_inicio_alternativas"]
    st.session_state["tempos_execucao"]["alternativas"] = round(tempo_final, 2)

    return matriz
