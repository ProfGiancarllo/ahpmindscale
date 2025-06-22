# exibir_resultado.py
import streamlit as st
import time

def exibir_resultado(final_scores, alternativas):
    melhor_idx = final_scores.argmax()
    melhor_alternativa = alternativas[melhor_idx]

    st.subheader("Resultado Final da Análise")
    
    # Exibe todas as pontuações
    for i, score in enumerate(final_scores):
        st.write(f"**{alternativas[i]}**: {score:.4f}")

    # Animação de destaque para o melhor resultado
    for _ in range(3):
        st.markdown(f"<h2 style='color:red; text-align:center;'>🏆 Melhor destino: {melhor_alternativa}</h2>", unsafe_allow_html=True)
        time.sleep(0.5)
        st.markdown(f"<h2 style='color:black; text-align:center;'>🏆 Melhor destino: {melhor_alternativa}</h2>", unsafe_allow_html=True)
        time.sleep(0.5)

    st.success(f"🏅 Decisão concluída com sucesso! Melhor alternativa: **{melhor_alternativa}**.")
