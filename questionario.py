# questionario.py
import streamlit as st
import csv
import os
from datetime import datetime
import pandas as pd

def carregar_tempos():
    tempos = st.session_state.get("tempos_execucao", {})
    inconsistencias = st.session_state.get("inconsistencias", 0)
    return tempos, inconsistencias


def exibir_questionario():
    st.header("📝 Questionário de Avaliação")

    tempos, inconsistencias = carregar_tempos()

    with st.form("form_questionario"):
        st.subheader("I. Identificação")
        email = st.text_input("1. Informe seu e-mail para receber os resultados:", max_chars=100)

        st.subheader("II. Avaliação de Carga Cognitiva – NASA-TLX (Raw-TLX)")
        mental = st.slider("2. Demanda Mental:", 0, 100, 50)
        fisica = st.slider("3. Demanda Física:", 0, 100, 50)
        temporal = st.slider("4. Demanda Temporal:", 0, 100, 50)
        desempenho = st.slider("5. Desempenho Percebido:", 0, 100, 50)
        esforco = st.slider("6. Esforço Geral:", 0, 100, 50)
        frustracao = st.slider("7. Frustração:", 0, 100, 50)

        st.subheader("III. Avaliação de Usabilidade – SUS (System Usability Scale)")
        sus = []
        afirmacoes = [
            "8. Eu gostaria de usar este sistema com frequência.",
            "9. Achei o sistema desnecessariamente complexo.",
            "10. Achei o sistema fácil de usar.",
            "11. Acho que precisaria da ajuda de um técnico para usar o sistema.",
            "12. As funcionalidades do sistema estão bem integradas.",
            "13. Achei o sistema muito inconsistente.",
            "14. A maioria das pessoas aprenderia a usar este sistema rapidamente.",
            "15. Achei o sistema muito confuso.",
            "16. Me senti confiante usando o sistema.",
            "17. Precisei aprender muitas coisas antes de conseguir usar o sistema."
        ]
        for i, texto in enumerate(afirmacoes):
            valor = st.radio(texto, [1, 2, 3, 4, 5], horizontal=True, key=f"sus_{i}")
            sus.append(valor)

        st.subheader("IV. Considerações Finais")
        concorda = st.radio("18. Você concorda com o resultado final da avaliação (destino escolhido)?",
                            ["Sim", "Não", "Parcialmente", "Não sei dizer"])
        comentario = st.text_area("19. Gostaria de deixar algum comentário sobre sua experiência?")

        enviar = st.form_submit_button("Enviar Respostas")

        if enviar:
            salvar_respostas(email, tempos, inconsistencias, mental, fisica, temporal,
                             desempenho, esforco, frustracao, sus, concorda, comentario)
            st.success("✅ Respostas enviadas com sucesso!")

    # Seção de acesso protegido para visualizar dados
    with st.expander("🔐 Acesso Administrativo"):
        senha = st.text_input("Digite a senha de acesso:", type="password")
        if senha == "@Bia250415":
            st.success("Acesso autorizado. Visualizando os dados armazenados:")
            try:
                df = pd.read_csv("dados/respostas_questionario.csv")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Erro ao carregar arquivo: {e}")
        elif senha:
            st.error("Senha incorreta.")

def salvar_respostas(email, tempos, inconsistencias, mental, fisica, temporal,
                     desempenho, esforco, frustracao, sus, concorda, comentario):
    diretorio = "dados"
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    arquivo = os.path.join(diretorio, "respostas_questionario.csv")
    existe = os.path.exists(arquivo)

    with open(arquivo, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        if not existe:
            writer.writerow([
                "DataHora", "Email",
                "Tempo_Criterios", "Tempo_Alternativas", "Inconsistencias",
                "Mental", "Fisica", "Temporal", "Desempenho", "Esforco", "Frustracao",
                *[f"SUS_{i+1}" for i in range(10)],
                "Concorda_Resultado", "Comentario"
            ])

        writer.writerow([
            datetime.now().isoformat(), email,
            tempos.get("criterios", ""), tempos.get("alternativas", ""), inconsistencias,
            mental, fisica, temporal, desempenho, esforco, frustracao,
            *sus,
            concorda, comentario
        ])
