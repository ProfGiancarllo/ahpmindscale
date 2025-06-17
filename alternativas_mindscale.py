import time
import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo


def comparar_alternativas_mindscale():
    iniciar_tempo("alternativas")
    if "criterios_concluidos" not in st.session_state or not st.session_state["criterios_concluidos"]:
        st.warning("Por favor, conclua a comparação entre critérios antes de avaliar as alternativas.")
        return

    if st.session_state["tempo_inicio_alternativas"] is None:
        st.session_state["tempo_inicio_alternativas"] = time.time()

    st.subheader("Etapa 2: Comparação entre Alternativas para cada Critério (MindScale)")
   
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
        1: "tem igual importância que",
        2: "é levemente mais importante que",
        3: "é um pouco mais importante que",
        4: "é moderadamente mais importante que",
        5: "é fortemente mais importante que",
        6: "é muito mais importante que",
        7: "é muito mais importante que (quase extremo)",
        8: "é extremamente mais importante que",
        9: "é absolutamente mais importante que"
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
        base = st.selectbox(f"Na sua opinião, considerando o critério '{criterio}', qual o melhor destino?", alternativas, key=f"base_{idx}")
        base_index = alternativas.index(base)

        comparacoes = {}

        for i in range(n_alt):
            if i != base_index:
                col1, col2 = st.columns([2, 3])
                with col1:
                     st.caption(f"🔎 {base}: {textos_apoio[criterio][base]}")
                     st.caption(f"🔍 {alternativas[i]}: {textos_apoio[criterio][alternativas[i]]}")
                with col2:
                     valor = st.slider(f"{alternativas[i]} vs {base}", min_value=1, max_value=9, value=5, key=f"comp_{idx}_{i}")
                     frase = legenda[valor]
                     st.markdown(f"**{valor}** – **{base}** {frase} **{alternativas[i]}**")

                     comparacoes[(i, base_index)] = round(1 / valor, 4)
                     comparacoes[(base_index, i)] = valor


        matriz = [[1.0 if i == j else None for j in range(n_alt)] for i in range(n_alt)]

        for (i, j), v in comparacoes.items():
            matriz[i][j] = v

        for i in range(n_alt):
            for j in range(n_alt):
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

        if all(matriz[i][j] is not None for i in range(n_alt) for j in range(n_alt)):
            pesos = calcular_pesos(matriz)
            CR = calcular_consistencia(matriz, pesos)
            if CR > 0.1:
               st.session_state["inconsistencias"] = st.session_state.get("inconsistencias", 0) + 1
            st.write(f"Razão de Consistência (CR): {CR:.4f}")
            if CR <= 0.1:
                st.success("✅ Matriz consistente")
                resultados[criterio] = pesos
                criterios_ok += 1
            else:
                st.error("❌ Matriz inconsistente. Ajuste os valores para melhorar a consistência.")
        else:
            st.warning("⚠️ Preencha todos os valores da matriz antes de prosseguir.")

    if criterios_ok == n_crit:
        st.session_state["alternativas_concluidas"] = True
        st.session_state["resultados_alternativas"] = resultados
        finalizar_tempo("alternativas")
        st.session_state["tempo_fim_alternativas"] = time.time()

        st.subheader("Resultado Final")
        scores_finais = np.zeros(n_alt)

        for idx, criterio in enumerate(criterios):
            scores_finais += np.array(resultados[criterio]) * pesos_criterios[idx]

        for i, score in enumerate(scores_finais):
            st.write(f"{alternativas[i]}: {score:.4f}")

        melhor = alternativas[np.argmax(scores_finais)]
        st.success(f"🏆 Melhor destino para viagem: **{melhor}**")
