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
import urllib.parse

# Defina os ENTRY IDs que encontramos no Google Forms (os seus reais IDs obtidos via inspecionar)
entry_metodo = "entry.1104627828"
entry_criterios = "entry.494086378"
entry_alternativas = "entry.1780294763"
entry_inconsistencias = "entry.1140431123"

# Monta o dicionário de parâmetros
parametros = {
    entry_metodo: st.session_state.get("metodo", ""),
    entry_criterios: st.session_state.get("tempo_criterios", ""),
    entry_alternativas: st.session_state.get("tempo_alternativas", ""),
    entry_inconsistencias: st.session_state.get("inconsistencias", ""),
}

# Codifica a URL com os parâmetros
params_codificados = urllib.parse.urlencode(parametros)

# ID do seu Google Form (copie o correto da sua URL)
google_form_id = "1FAIpQLScDn-iexyubiO_wZ1Lqei6AT5thX88MvedT8XIvmmd_zLmvjA"

# Monta a URL final
url_forms = f"https://docs.google.com/forms/d/e/{google_form_id}/viewform?{params_codificados}"

# Exibe o botão para o usuário enviar as respostas
if st.button("Enviar dados para o Google Forms"):
    st.markdown(f"[Clique aqui para enviar suas respostas]({url_forms})", unsafe_allow_html=True)
