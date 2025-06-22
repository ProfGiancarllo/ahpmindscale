# alternativas_tradicional.py
from email.mime import base
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo

def comparar_alternativas_tradicional():
    iniciar_tempo("alternativas")

    if "criterios_concluidos" not in st.session_state or not st.session_state["criterios_concluidos"]:
        st.warning("Por favor, conclua a comparação entre critérios antes de avaliar as alternativas.")
        return

    st.subheader("Etapa 2: Comparação entre Alternativas para cada Critério (Método Tradicional)")
    
    alternativas = [
        "Nova York (EUA)",
        "Orlando (Disney - EUA)",
        "Paris (França)",
        "Londres (Reino Unido)",
        "Roma (Itália)",
        "Tóquio (Japão)"
    ]
    n_alt = len(alternativas)

    criterios = st.session_state["nomes_criterios"]
    pesos_criterios = st.session_state["pesos_criterios"]
    n_crit = len(criterios)

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
    textos_apoio = {
        "Custo da Viagem": {
            "Nova York (EUA)": "Custo médio de R$ 18.000, incluindo passagem, hospedagem e alimentação.",
            "Orlando (Disney - EUA)": "Custo médio de R$ 20.000, incluindo ingressos dos parques.",
            "Paris (França)": "Custo médio de R$ 17.000, considerando atrações e alimentação.",
            "Londres (Reino Unido)": "Custo médio de R$ 19.000 com libra mais valorizada.",
            "Roma (Itália)": "Custo médio de R$ 16.000, com opções econômicas disponíveis.",
            "Tóquio (Japão)": "Custo médio de R$ 21.000, devido à longa distância e custo de vida."
        },
        "Belezas Naturais": {
            "Nova York (EUA)": "Central Park e Niagara Falls (viagem extra).",
            "Orlando (Disney - EUA)": "Parques temáticos com áreas verdes e lagos artificiais.",
            "Paris (França)": "Jardins de Luxemburgo e parques urbanos.",
            "Londres (Reino Unido)": "Hyde Park e excursões para Cotswolds.",
            "Roma (Itália)": "Jardins de Villa Borghese e proximidade com a Toscana.",
            "Tóquio (Japão)": "Monte Fuji próximo, jardins imperiais e parques floridos."
        },
        "Atrativos Culturais": {
            "Nova York (EUA)": "Museus como MoMA e MET, Broadway e arquitetura icônica.",
            "Orlando (Disney - EUA)": "Foco em entretenimento, com atrações temáticas.",
            "Paris (França)": "Museu do Louvre, Torre Eiffel, e grande acervo histórico.",
            "Londres (Reino Unido)": "British Museum, Torre de Londres, tradição e modernidade.",
            "Roma (Itália)": "Coliseu, Vaticano, e herança romana e renascentista.",
            "Tóquio (Japão)": "Templos antigos, museus modernos e tradição milenar."
        },
        "Gastronomia": {
            "Nova York (EUA)": "Culinária internacional e opções gourmet de alto nível.",
            "Orlando (Disney - EUA)": "Comida americana, temática e redes internacionais.",
            "Paris (França)": "Alta gastronomia francesa, cafés e vinhos renomados.",
            "Londres (Reino Unido)": "Culinária internacional, bons restaurantes e pubs.",
            "Roma (Itália)": "Massas, pizzas autênticas e culinária italiana clássica.",
            "Tóquio (Japão)": "Sushi, ramen, izakayas e cozinha japonesa tradicional."
        },
        "Compras": {
            "Nova York (EUA)": "5ª Avenida, outlets e variedade de marcas famosas.",
            "Orlando (Disney - EUA)": "Outlets com grandes descontos e lojas de lembranças.",
            "Paris (França)": "Moda de luxo, boutiques e grandes lojas como Galeries Lafayette.",
            "Londres (Reino Unido)": "Oxford Street, lojas vintage e centros comerciais.",
            "Roma (Itália)": "Moda italiana, mercados locais e lojas de grife.",
            "Tóquio (Japão)": "Tecnologia, moda japonesa e centros comerciais modernos."
        }
    }

    resultados = {}
    criterios_ok = 0

    for idx, criterio in enumerate(criterios):
        st.markdown(f"### Compare as alternativas segundo o critério '{criterio}', não tenha pressa, consulte as informações apresentadas e a legenda")
        matriz = [[1 if i == j else None for j in range(n_alt)] for i in range(n_alt)]

        for i in range(n_alt):
            for j in range(i + 1, n_alt):
                col1, col2 = st.columns([2, 3])
                with col1:
                     st.caption(f"🔎 {alternativas[j]}: {textos_apoio[criterio][alternativas[j]]}")
                     st.caption(f"🔍 {alternativas[i]}: {textos_apoio[criterio][alternativas[i]]}")

                with col2:
                     valor = st.select_slider(
                        f"{alternativas[i]} vs {alternativas[j]} ({criterio})",
                        options=[1/9, 1/7, 1/5, 1/3, 1, 3, 5, 7, 9],
                        value=1,
                        format_func=lambda x: f"{round(x, 3)}",
                        key=f"alt_{idx}_{i}_{j}"
                     )
                     matriz[i][j] = valor
                     matriz[j][i] = round(1 / valor, 4)

                     if valor == 1:
                        frase = legenda[1]
                        st.markdown(f"**{round(valor, 3)}** – **{alternativas[i]}** tem {frase} a **{alternativas[j]}**")
                     elif valor > 1:
                        frase = legenda[int(valor)]
                        st.markdown(f"**{int(valor)}** – **{alternativas[i]}** tem {frase} a **{alternativas[j]}**")
                     else:
                        frase = legenda[int(round(1 / valor))]
                        st.markdown(f"**{round(valor, 3)}** – **{alternativas[j]}** tem {frase} a **{alternativas[i]}**")

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

        if all(matriz[i][j] is not None for i in range(n_alt) for j in range(n_alt)):
            pesos = calcular_pesos(matriz)
            CR = calcular_consistencia(matriz, pesos)

            st.write(f"Razão de Consistência (CR): {CR:.4f}")
            if CR <= 0.1:
                st.success("✅ Matriz consistente")
                resultados[criterio] = pesos
                criterios_ok += 1
            else:
                st.error("❌ Matriz inconsistente. Ajuste os valores para melhorar a consistência.")
                st.session_state["inconsistencias"] += 1
        else:
            st.warning("⚠️ Preencha todos os valores da matriz antes de prosseguir.")

   from exibir_resultado import exibir_resultado_final

if criterios_ok == n_crit:
    st.session_state["alternativas_concluidas"] = True
    st.session_state["resultados_alternativas"] = resultados
    finalizar_tempo("alternativas")

    exibir_resultado_final(alternativas, resultados, pesos_criterios, criterios)
