import streamlit as st
from chatbot import gerar_resposta
import pandas as pd
import os

# Configuração da página
st.set_page_config(page_title="Chatbot de Consulta de Dados (LangChain/Pandas)", layout="wide")

# Título e descrição
st.title("🤖 Chatbot de Consulta de Dados")
st.markdown(
    """
    Este chatbot utiliza **LangChain** e **Pandas** para responder a perguntas
    sobre o seu arquivo de dados (`data.csv`).
    
    **Suporta múltiplos provedores:** OpenAI, Ollama (gratuito/local), Google Gemini (gratuito)
    
    Faça perguntas em linguagem natural sobre os dados, e o agente irá gerar e executar
    o código Python necessário para obter a resposta.
    
    **Configure o provedor no arquivo `.env` usando a variável `LLM_PROVIDER`**
    """
)

# Mostra qual provedor está sendo usado
llm_provider = os.getenv("LLM_PROVIDER", "openai").upper()
st.info(f"🔧 Provedor LLM configurado: **{llm_provider}**")

# --- Carregamento e Exibição do DataFrame ---
CSV_FILE_PATH = "data.csv"
# Suporte para CSV via URL (útil para Streamlit Cloud)
CSV_URL = os.getenv("CSV_URL", None)

try:
    # Tenta carregar de URL primeiro (para Streamlit Cloud), depois do arquivo local
    if CSV_URL:
        df = pd.read_csv(CSV_URL)
    else:
        df = pd.read_csv(CSV_FILE_PATH)
    st.subheader("Amostra do DataFrame Carregado")
    st.dataframe(df.head())
    st.info(f"DataFrame carregado com sucesso: {df.shape[0]} linhas e {df.shape[1]} colunas.")
except FileNotFoundError:
    st.error(f"Erro: Arquivo CSV não encontrado em {CSV_FILE_PATH}. Certifique-se de que 'data.csv' está no diretório correto.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar o DataFrame: {e}")
    st.stop()

# --- Inicialização do Histórico de Conversa ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Olá! Eu sou um agente de dados. Pergunte-me algo sobre o DataFrame acima!"})

if "raciocinios" not in st.session_state:
    st.session_state.raciocinios = {}

# --- Exibição do Histórico de Conversa ---
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        # Verifica se é uma mensagem de erro
        if message["content"].startswith(("⚠️", "🔑", "❌")):
            st.error(message["content"])
        else:
            st.markdown(message["content"])
    
    # Exibe o raciocínio fora do chat_message para evitar problemas de renderização
    if message["role"] == "assistant" and i in st.session_state.raciocinios:
        raciocinio = st.session_state.raciocinios[i]
        if raciocinio and raciocinio.strip():
            with st.expander("🔍 Raciocínio (Código Python Gerado)", expanded=False):
                st.code(raciocinio, language="python")

# --- Entrada do Usuário ---
if prompt := st.chat_input("Digite sua pergunta sobre os dados..."):
    # 1. Adiciona a mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Renderiza a mensagem do usuário imediatamente
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 3. Gera a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            try:
                resposta_final, raciocinio = gerar_resposta(prompt)
            except Exception as e:
                resposta_final = f"❌ **Erro inesperado:** {str(e)}"
                raciocinio = ""
        
        # Verifica se é uma mensagem de erro
        if resposta_final.startswith(("⚠️", "🔑", "❌")):
            st.error(resposta_final)
        else:
            st.markdown(resposta_final)
        
        # Exibe o raciocínio se houver
        if raciocinio and raciocinio.strip():
            with st.expander("🔍 Raciocínio (Código Python Gerado)", expanded=False):
                st.code(raciocinio, language="python")
    
    # 4. Adiciona a resposta do assistente ao histórico
    indice_resposta = len(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": resposta_final})
    
    # 5. Armazena o raciocínio se houver
    if raciocinio and raciocinio.strip():
        st.session_state.raciocinios[indice_resposta] = raciocinio

# --- Aviso sobre a Chave da API ---
llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()
if llm_provider == "openai" and not os.getenv("OPENAI_API_KEY"):
    st.warning("⚠️ A chave `OPENAI_API_KEY` não foi encontrada. Certifique-se de que ela está definida no arquivo `.env`")
elif llm_provider == "gemini" and not os.getenv("GOOGLE_API_KEY"):
    st.warning("⚠️ A chave `GOOGLE_API_KEY` não foi encontrada. Obtenha uma em: https://makersuite.google.com/app/apikey")
elif llm_provider == "ollama":
    st.info("✅ Usando Ollama (gratuito). Certifique-se de que o Ollama está rodando: `ollama serve`")
