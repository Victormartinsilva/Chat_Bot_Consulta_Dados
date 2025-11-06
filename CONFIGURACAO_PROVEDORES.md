# 🤖 Configuração de Provedores LLM

Este chatbot suporta múltiplos provedores de LLM, incluindo opções **100% gratuitas**!

## 📋 Opções Disponíveis

### 1. 🟢 **Ollama (RECOMENDADO - 100% Gratuito)**
- **Vantagem:** Totalmente gratuito, roda localmente na sua máquina
- **Desvantagem:** Requer instalação e pode ser mais lento
- **Instalação:**
  1. Baixe e instale: https://ollama.ai/
  2. Baixe um modelo: `ollama pull llama3.2`
  3. Inicie o servidor: `ollama serve`

**Configuração no `.env`:**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

### 2. 🟡 **Google Gemini (Gratuito)**
- **Vantagem:** Gratuito, rápido, não precisa instalar nada
- **Desvantagem:** Requer API key (mas é gratuita)
- **Obtenção da API Key:**
  1. Acesse: https://makersuite.google.com/app/apikey
  2. Faça login com sua conta Google
  3. Crie uma nova API key

**Configuração no `.env`:**
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_google_aqui
GEMINI_MODEL=gemini-pro
```

### 3. 🔵 **OpenAI (Pago)**
- **Vantagem:** Melhor qualidade, mais rápido
- **Desvantagem:** Requer créditos pagos
- **Obtenção da API Key:**
  1. Acesse: https://platform.openai.com/api-keys
  2. Crie uma nova API key
  3. Adicione créditos à sua conta

**Configuração no `.env`:**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-3.5-turbo
```

## 🚀 Como Configurar

1. **Abra o arquivo `.env`** na pasta do projeto
2. **Adicione as variáveis** conforme o provedor escolhido acima
3. **Reinicie o Streamlit** para aplicar as mudanças

## 💡 Qual Escolher?

- **Quer algo 100% gratuito?** → Use **Ollama**
- **Quer algo rápido e fácil?** → Use **Google Gemini**
- **Quer a melhor qualidade?** → Use **OpenAI** (pago)

## 🔧 Instalação de Dependências

Para usar Ollama ou Gemini, instale as dependências adicionais:

```bash
pip install langchain-community langchain-google-genai
```

Ou simplesmente:

```bash
pip install -r requirements.txt
```

