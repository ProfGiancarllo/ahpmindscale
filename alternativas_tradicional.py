import streamlit as st
import numpy as np
from registro_tempo import iniciar_tempo, finalizar_tempo

def comparar_alternativas_tradicional():
    iniciar_tempo("alternativas")

    if "criterios_concluidos" not in st.session_state or not st.session_state["criterios_concluidos"]:
        st.warning("Por favor, conclua a comparação entre critérios antes de avaliar as alternativas.")
        return

    st.subheader("Etapa 2: Comparação entre Alternativas para cada Critério (Tradicional)")
    st.subheader("Compare as alternativas segundo a escala apresentada, não tenha pressa, siga no seu tempo")

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

    valores_saaty = [1/9, 1/8, 1/7, 1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    rotulos_saaty = ["1/9", "1/8", "1/7", "1/6", "1/5", "1/4", "1/3", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    legenda = {
        "9": "é absolutamente mais importante que",
        "8": "é quase absolutamente mais importante que",
        "7": "é extremamente mais importante que",
        "6": "é fortemente mais importante que",
        "5": "é muito mais importante que",
        "4": "é moderadamente mais importante que",
        "3": "é um pouco mais importante que",
        "2": "é levemente mais importante que",
        "1": "tem igual importância que",
        "1/2": "é levemente menos importante que",
        "1/3": "é um pouco menos importante que",
        "1/4": "é moderadamente menos importante que",
        "1/5": "é muito menos importante que",
        "1/6": "é fortemente menos importante que",
        "1/7": "é extremamente menos importante que",
        "1/8": "é quase absolutamente menos importante que",
        "1/9": "é absolutamente menos importante que"
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
        st.markdown(f"### Critério: {criterio}")
        matriz = [[1 if i == j else None for j in range(n_alt)] for i in range(n_alt)]

        for i in range(n_alt):
            for j in range(i + 1, n_alt):
                col1, col2 = st.columns([3, 2])
                with col1:
                    idx_valor = st.slider(
                        f"{alternativas[i]} vs {alternativas[j]} ({criterio})",
                        min_value=0, max_value=16, value=8,
                        format="%s", key=f"alt_{idx}_{i}_{j}")
                    valor = valores_saaty[idx_valor]
                    matriz[i][j] = valor
                    matriz[j][i] = round(1 / valor, 4)
                with col2:
                    frase = legenda[rotulos_saaty[idx_valor]].replace("tem", f"de {alternativas[i]} tem")
                    st.markdown(f"**{rotulos_saaty[idx_valor]}** – {alternativas[i]} {frase} em relação a {alternativas[j]}")
                    st.caption(f"🔎 {alternativas[j]}: {textos_apoio[criterio][alternativas[j]]}\n\n🔍 {alternativas[i]}: {textos_apoio[criterio][alternativas[i]]}")

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
            RI_dict = { 1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49 }
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

    if criterios_ok == n_crit:
        st.session_state["alternativas_concluidas"] = True
        st.session_state["resultados_alternativas"] = resultados
        finalizar_tempo("alternativas")
        st.subheader("Resultado Final")
        scores_finais = np.zeros(n_alt)

        for idx, criterio in enumerate(criterios):
            scores_finais += np.array(resultados[criterio]) * pesos_criterios[idx]

        for i, score in enumerate(scores_finais):
            st.write(f"{alternativas[i]}: {score:.4f}")

        melhor = alternativas[np.argmax(scores_finais)]
        st.markdown(f"<h1 style='text-align: center; color: green; font-size: 40px;'>🏆 Melhor destino: {melhor}</h1>", unsafe_allow_html=True)
