 AhpMindScale – Sistema Interativo de Apoio à Decisão Multicritério

Versão: 1.00  
Autores: Giancarllo Ribeiro Vasconcelos, Caroline Maria de Miranda Mota  

AhpMindScale é um sistema web de apoio à decisão multicritério baseado no método Analytic Hierarchy Process (AHP), com foco em reduzir a inconsistência dos julgamentos e a carga cognitiva associada às comparações par a par.

O software foi desenvolvido no contexto de um projeto de doutorado em Engenharia de Produção e implementa um modelo interativo de elicitação de preferências, combinando:

- Construção parcial da matriz de comparações com apoio de Matriz Recíproca Transitiva (RTM);  
- Ajuste interativo de preferências, guiado por feedback em tempo real sobre a inconsistência dominante;  
- Interface amigável, com escala reduzida e fluxo de interação pensado para usuários leigos e especialistas.



 📚 Sumário

1. Visão geral  
2. Arquitetura e tecnologias  
3. Funcionalidades principais  
4. Estrutura do repositório  
5. Requisitos  
6. Instalação e execução  
7. Fluxo de uso do sistema  
8. Armazenamento e arquivos gerados  
9. Uso em pesquisa acadêmica  
10. Roadmap e limitações  
11. Licença  
12. Contato  



 🌐 Visão geral

O AhpMindScale foi concebido para endereçar um problema clássico do AHP:  
à medida que o número de critérios e alternativas cresce, a inconsistência dos julgamentos aumenta e o esforço mental do decisor se torna elevado.

Para isso, o sistema:

- Reduz o número de comparações por meio da construção parcial da matriz e do uso de RTM;  
- Identifica automaticamente as comparações mais problemáticas, permitindo que o usuário revise apenas os pontos críticos;  
- Oferece uma experiência guiada, com telas sequenciais e mensagens claras, reduzindo a sensação de complexidade do método AHP tradicional.

O foco inicial da aplicação é a simulação de decisões com múltiplos critérios (por exemplo, seleção de alternativas de viagem), mas o modelo é geral e pode ser adaptado para outros contextos de decisão multicritério (portfólio de projetos, seleção de fornecedores, priorização de iniciativas, etc.).



 🏗 Arquitetura e tecnologias

O AhpMindScale segue uma arquitetura em três camadas:

1. Frontend (Interface do Usuário)  
   - HTML5, CSS3 e elementos de JavaScript  
   - Páginas específicas para:
     - Comparações no modelo tradicional (escala completa)
     - Comparações no modelo MindScale (escala reduzida, fluxo interativo)
     - Apresentação de resultados (pesos, índice de consistência, etc.)

2. Backend (Lógica de Negócio)  
   - Python  
   - Flask (microframework web)  
   - Responsável por:
     - Controle das rotas da aplicação  
     - Seleção aleatória dos pares a serem comparados  
     - Aplicação das rotinas de verificação de consistência e transitividade  
     - Construção da matriz de decisão  
     - Cálculo dos vetores de prioridades e do índice de consistência  
     - Registro de julgamentos em arquivos CSV

3. Camada de Armazenamento (Dados e Resultados)  
   - Arquivos CSV armazenados localmente  
   - Separação entre respostas do método tradicional e do método MindScale  
   - Rotina automática de limpeza dos dados ao início de cada nova sessão de uso (para evitar interferência entre testes).



 ⚙ Funcionalidades principais

- Comparação par a par – Versão Tradicional (AHP clássico)  
  - Escala completa baseada na escala de Saaty  
  - Construção exaustiva da matriz de comparações

- Comparação par a par – Versão MindScale  
  - O usuário primeiro indica qual alternativa é melhor  
  - Em seguida, usa um controle deslizante (slider) com escala reduzida, sempre favorecendo a alternativa previamente escolhida  
  - As demais entradas da matriz são preenchidas automaticamente com base na Matriz Recíproca Transitiva (RTM)  
  - O sistema monitora a inconsistência dominante e sugere ajustes locais

- Cálculo automático de resultados
  - Vetores de pesos para critérios e alternativas  
  - Índice de consistência (IC/CR)  
  - Ranking final das alternativas

- Interface guiada e experimento controlado
  - Tela inicial explicativa  
  - Sequência de telas para:
    1. Comparação de critérios  
    2. Comparação de alternativas  
    3. Exibição dos resultados  
    4. Link para questionários externos (NASA-TLX, SUS, etc., quando utilizado em estudo experimental)



 🗂 Estrutura do repositório

> *Observação*: adapte este bloco conforme a estrutura real do seu repositório.

```text
AHP-MindScale-v1_00/
├─ app.py                     Arquivo principal Flask (ponto de entrada da aplicação)
├─ mindscale_core.py          Implementação do algoritmo MindScale (lógica de comparação e ajuste)
├─ ahp_tradicional.py         Rotinas auxiliares para o AHP tradicional
├─ requirements.txt           Dependências Python do projeto
├─ README.md                  Este arquivo
├─ /templates                 Templates HTML (Flask)
│   ├─ index.html             Tela inicial / apresentação do sistema
│   ├─ comparar_tradicional.html   Tela de comparações (modelo tradicional)
│   ├─ comparar_mindscale.html     Tela de comparações (modelo MindScale)
│   ├─ resultado.html         Tela de apresentação dos resultados
├─ /static                    Arquivos estáticos (CSS, JS, imagens)
│   ├─ css/
│   │   └─ style.css
│   ├─ js/
│   │   └─ script.js
│   └─ img/
│       └─ ...
└─ /data                      Dados de entrada e saída
    ├─ respostas_ahp.csv          Respostas do modelo tradicional
    ├─ respostas_mindscale.csv    Respostas do modelo MindScale
    └─ ...
```



 💻 Requisitos

- Python 3.8+ (recomendado)  
- Sistema operacional:
  - Windows, Linux ou macOS  
- Bibliotecas Python principais:
  - `flask`  
  - `numpy`  
  - `pandas`  
  - Outras dependências listadas no arquivo `requirements.txt`

Exemplo de `requirements.txt` (ajuste conforme seu projeto real):

```txt
flask
numpy
pandas
```



 🚀 Instalação e execução

 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

Ou baixe o ZIP pelo GitHub e extraia para uma pasta, por exemplo:  
`AHP-MindScale-v1_00/`.

 2. Criar e ativar um ambiente virtual (opcional, mas recomendado)

Windows (PowerShell ou CMD):

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

 4. Configurar variáveis de ambiente (se necessário)

Se estiver usando Flask como ponto de entrada:

Windows:

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
```

Linux / macOS:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

 5. Executar a aplicação

```bash
flask run
```

ou, dependendo de como o `app.py` foi escrito:

```bash
python app.py
```

A aplicação geralmente ficará disponível em:

> http://127.0.0.1:5000/  

Abra o navegador e acesse esse endereço para utilizar o AhpMindScale localmente.



 🔄 Fluxo de uso do sistema

1. Página inicial (`/`)
   - Apresenta o objetivo do sistema e o contexto de uso
   - Botão “Iniciar Avaliação”

2. Rota `/comparar`
   - Redireciona aleatoriamente o usuário para:
     - `/comparar-tradicional`, ou
     - `/comparar-mindscale`
   - Usado em experimentos para balancear grupos (controle x experimental)

3. Rota `/comparar-tradicional`
   - Interface com escala completa (AHP clássico)
   - Usuário realiza comparações par a par de forma exaustiva

4. Rota `/comparar-mindscale`
   - Fluxo interativo em duas etapas:
     1. Escolha da alternativa preferida
     2. Ajuste da intensidade com um slider em escala reduzida, sempre no sentido da alternativa já escolhida
   - Preenchimento automático das demais entradas pela regra de transitividade e RTM

5. Rota `/resultado`
   - Processa as respostas registradas nos arquivos CSV
   - Calcula:
     - Matriz de decisão
     - Vetores de pesos
     - Índice de consistência
     - Ranking das alternativas
   - Exibe os resultados ao usuário de forma clara

6. (Opcional) Questionário externo
   - Ao final, o sistema pode apresentar um link para questionário (ex.: Google Forms) para coleta de dados de:
     - Carga cognitiva (NASA-TLX)
     - Usabilidade (SUS)
     - Satisfação com o resultado



 📁 Armazenamento e arquivos gerados

Na pasta `/data` (ou equivalente), o sistema grava os julgamentos em arquivos CSV:

- `respostas_ahp.csv`  
  - Comparações realizadas pelo grupo que usa o método tradicional

- `respostas_mindscale.csv`  
  - Comparações realizadas pelo grupo que usa o método AhpMindScale

Esses arquivos podem ser importados em ferramentas como:

- Python (pandas)
- R
- Excel
- Jamovi / JASP (via CSV)

para análise estatística, cálculo adicional de indicadores, validações e replicação de resultados.



 🎓 Uso em pesquisa acadêmica

O AhpMindScale foi originalmente desenvolvido como parte de uma tese de doutorado em Engenharia de Produção, com estudo de caso em seleção de portfólio de projetos e experimento com grupos controle e experimental.

Se você utilizar o AhpMindScale em pesquisas científicas ou trabalhos acadêmicos, recomenda-se citar a tese e/ou artigos associados (adapte para o formato bibliográfico desejado):

```text
VASCONCELOS, G. R.; MOTA, C. M. M. Modelo interativo de ajuste de preferências em decisão multicritério: redução da inconsistência em comparações par a par no AHP. Tese (Doutorado em Engenharia de Produção), 2025.
```

> *Substitua pelos dados finais de publicação assim que a tese estiver oficialmente depositada e/ou houver artigos publicados sobre o AhpMindScale.*



 🧭 Roadmap e limitações

 Possíveis evoluções

- Internacionalização da interface (pt-BR / en)  
- Módulo de análise de sensibilidade integrado ao frontend  
- Persistência em banco de dados (ex.: SQLite, PostgreSQL) em vez de CSV  
- Autenticação de usuários e histórico de decisões  
- Integração com outros métodos multicritério (ex.: SMART, TOPSIS, etc.)

 Limitações atuais

- Aplicação orientada inicialmente a estudos controlados e prototipagem
- Persistência via arquivos CSV locais (não pensada, nesta versão, para uso multiusuário em produção)
- Escala e parâmetros calibrados a partir de um contexto experimental específico (seleção de alternativas de viagem / portfólio)



 📜 Licença

> Importante: defina explicitamente a licença que você deseja adotar.

Sugestões comuns (escolha e ajuste o texto abaixo):

- Uso acadêmico apenas:  
  > Este software é disponibilizado exclusivamente para fins acadêmicos e de pesquisa. Qualquer uso comercial requer autorização expressa dos autores.

- Ou licença padrão, como MIT / GPL / etc.:  
  - Adicione aqui o texto da licença escolhida  
  - E, preferencialmente, crie um arquivo separado `LICENSE` no repositório.



 📫 Contato

Para dúvidas, sugestões ou colaborações relacionadas ao AhpMindScale:

- Autor: Giancarllo Ribeiro Vasconcelos  
- E-mail: giancarllo@unirv.edu.br  

Sinta-se à vontade para abrir *issues* ou *pull requests* neste repositório, caso deseje contribuir com melhorias, correções ou novas funcionalidades para o AhpMindScale.
