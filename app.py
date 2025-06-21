# app.py
import streamlit as st
import random
variaveis_sessao = {
    "tempo_inicio_criterios": None,
    "tempo_fim_criterios": None,
    "tempo_inicio_alternativas": None,
    "tempo_fim_alternativas": None,
    "criterios_concluidos": False,
    "alternativas_concluidas": False,
    "inconsistencias": 0,
    "tempos_execucao": {}
}

for chave, valor_padrao in variaveis_sessao.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor_padrao
for chave in [
    "tempo_inicio_criterios", 
    "tempo_fim_criterios", 
    "tempo_inicio_alternativas", 
    "tempo_fim_alternativas", 
    "criterios_concluidos", 
    "alternativas_concluidas", 
    "inconsistencias",
    "tempos_execucao"
]:
    if chave not in st.session_state:
        st.session_state[chave] = None if "tempo" in chave else 0 if chave == "inconsistencias" else False
from criterios_tradicional import comparar_criterios_tradicional
from criterios_mindscale import comparar_criterios_mindscale
from alternativas_tradicional import comparar_alternativas_tradicional
from alternativas_mindscale import comparar_alternativas_mindscale
from questionario import exibir_questionario
from registro_tempo import resetar_tempos

st.set_page_config(page_title="AHP com Fluxo Automatizado", layout="centered")

if "etapa" not in st.session_state:
    st.session_state.etapa = 0
if "metodo" not in st.session_state:
    st.session_state.metodo = None
if "criterios_concluidos" not in st.session_state:
    st.session_state.criterios_concluidos = False
if "alternativas_concluidas" not in st.session_state:
    st.session_state.alternativas_concluidas = False
if "inconsistencias" not in st.session_state:
    st.session_state.inconsistencias = 0

if st.session_state.etapa == 0:
    st.image("logoahpmindscale.png", width=180)  # substitua com o nome real se for diferente
    st.title("🧠 Bem-vindo ao AhpMindScale")

    st.markdown("""
            Olá! 👋

            Você está prestes a participar de um experimento que compara duas formas de tomada de decisão baseadas no método AHP (Analytic Hierarchy Process). O objetivo é entender como diferentes formas de interação influenciam a qualidade dos julgamentos e a experiência do usuário.

            Ao longo do processo, você irá:

            ✅ Comparar alternativas ou critérios em pares, escolhendo qual é melhor segundo sua percepção.  
            ✅ Utilizar uma escala intuitiva e simplificada (MindScale) ou a escala tradicional do AHP.  
            ✅ Avaliar sua experiência ao final, com perguntas sobre facilidade de uso, esforço mental e satisfação.

            ⏱️ O sistema irá registrar o tempo de resposta e a consistência dos seus julgamentos automaticamente.  
            🔒 Todas as suas respostas serão mantidas em sigilo e utilizadas exclusivamente para fins acadêmicos.

            > ⚠️ **Importante:** Não há respostas certas ou erradas. O que importa é sua percepção e experiência.  
            > 💡 Seja sincero e siga seu raciocínio natural.

            Quando estiver pronto(a), clique em **Iniciar** e siga as instruções da tela. Obrigado por contribuir com esta pesquisa!
            """)
    if st.button("Iniciar Avaliação"):
        st.session_state.metodo = random.choice(["tradicional", "mindscale"])
        st.session_state.etapa = 1
        resetar_tempos()
        st.rerun()

elif st.session_state.etapa == 1:
    if st.session_state.metodo == "tradicional":
        comparar_criterios_tradicional()
    else:
        comparar_criterios_mindscale()

    if st.session_state.criterios_concluidos:
        if st.button("👉 Seguir à próxima etapa"):
            st.session_state.etapa = 2
            st.rerun()

elif st.session_state.etapa == 2:
    if st.session_state.metodo == "tradicional":
        comparar_alternativas_tradicional()
    else:
        comparar_alternativas_mindscale()

    if st.session_state.alternativas_concluidas:
        if st.button("👉 Seguir à próxima etapa"):
            st.session_state.etapa = 3
            st.rerun()

elif st.session_state.etapa == 3:
    exibir_questionario()
    if st.button("👉 Finalizar"):
        st.session_state.etapa = 4
        st.rerun()

elif st.session_state.etapa == 4:
    st.success("✅ Processo finalizado. Obrigado por participar!")
    if st.button("Refazer Avaliação"):
        for chave in list(st.session_state.keys()):
            del st.session_state[chave]
        st.rerun()
