# 🤖 Chatbot de Consulta de Dados

Um chatbot inteligente desenvolvido com **Streamlit**, **LangChain** e **Pandas** para responder perguntas sobre dados em linguagem natural.

## ✨ Funcionalidades

- 💬 Interface de chat intuitiva e moderna
- 📊 Análise de dados em linguagem natural
- 🐍 Geração automática de código Python para análise
- 🔄 Suporte a múltiplos provedores LLM:
  - **OpenAI** (GPT-3.5, GPT-4)
  - **Google Gemini** (gratuito)
  - **Ollama** (gratuito, local)

## 🚀 Deploy no Streamlit Cloud

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Arquivo CSV com dados (`data.csv`)

## 🔧 Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Victormartinsilva/Chat_Bot_Consulta_Dados.git
   cd Chat_Bot_Consulta_Dados/Chat_Bot/Chat_Bot
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=sua_chave_aqui
   GEMINI_MODEL=gemini-2.5-flash
   ```

4. **Coloque seu arquivo CSV:**
   - Renomeie seu arquivo para `data.csv`
   - Coloque na mesma pasta do `app.py`

5. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

## ⚙️ Configuração dos Provedores LLM

### Google Gemini (Recomendado - Gratuito)

1. Obtenha sua API key em: https://makersuite.google.com/app/apikey
2. Configure no `.env`:
   ```env
   LLM_PROVIDER=gemini
   GOOGLE_API_KEY=sua_chave_aqui
   GEMINI_MODEL=gemini-2.5-flash
   ```

### OpenAI

1. Obtenha sua API key em: https://platform.openai.com/api-keys
2. Configure no `.env`:
   ```env
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sua_chave_aqui
   OPENAI_MODEL=gpt-3.5-turbo
   ```

### Ollama (Local)

1. Instale o Ollama: https://ollama.ai
2. Baixe um modelo: `ollama pull llama3.2`
3. Configure no `.env`:
   ```env
   LLM_PROVIDER=ollama
   OLLAMA_MODEL=llama3.2
   OLLAMA_BASE_URL=http://localhost:11434
   ```

## 📁 Estrutura do Projeto

```
Chat_Bot_Consulta_Dados/
├── Chat_Bot/
│   └── Chat_Bot/
│       ├── app.py                    # Aplicação Streamlit principal
│       ├── chatbot.py                # Lógica do agente LangChain
│       ├── requirements.txt          # Dependências Python
│       ├── data.csv                  # Arquivo de dados (não versionado)
│       ├── .env                      # Variáveis de ambiente (não versionado)
│       ├── README.md                 # Este arquivo
│       └── .gitignore                # Arquivos ignorados pelo Git
```

## 🌐 Deploy no Streamlit Cloud

### Passo 1: Preparar o Repositório

1. Certifique-se de que todos os arquivos estão commitados
2. Faça push para o GitHub

### Passo 2: Conectar ao Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em "New app"
4. Selecione seu repositório: `Victormartinsilva/Chat_Bot_Consulta_Dados`
5. Configure:
   - **Main file path:** `Chat_Bot/Chat_Bot/app.py`
   - **Python version:** 3.11

### Passo 3: Configurar Secrets

No Streamlit Cloud, vá em "Settings" → "Secrets" e adicione:

```toml
LLM_PROVIDER = "gemini"
GOOGLE_API_KEY = "sua_chave_aqui"
GEMINI_MODEL = "gemini-2.5-flash"
```

### Passo 4: Fazer Upload do CSV

1. No Streamlit Cloud, vá em "Settings" → "Files"
2. Faça upload do arquivo `data.csv`

**OU** configure para ler de uma URL:

```python
# No app.py, adicione suporte para URL
CSV_URL = st.secrets.get("CSV_URL", None)
if CSV_URL:
    df = pd.read_csv(CSV_URL)
else:
    df = pd.read_csv("data.csv")
```

## 📝 Exemplos de Uso

- "Quantas linhas tem o DataFrame?"
- "Quais são as colunas disponíveis?"
- "Mostre os 10 primeiros registros"
- "Qual é a média da coluna X?"
- "Quantos valores únicos existem na coluna Y?"

## 🛠️ Tecnologias Utilizadas

- **Streamlit** - Framework web para Python
- **LangChain** - Framework para aplicações LLM
- **Pandas** - Manipulação e análise de dados
- **Google Gemini API** - Modelo de linguagem
- **OpenAI API** - Modelo de linguagem (alternativa)
- **Ollama** - Modelo de linguagem local (alternativa)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

**Victor Silva**
- GitHub: [@Victormartinsilva](https://github.com/Victormartinsilva)
- Repositório: [Chat_Bot_Consulta_Dados](https://github.com/Victormartinsilva/Chat_Bot_Consulta_Dados)

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
