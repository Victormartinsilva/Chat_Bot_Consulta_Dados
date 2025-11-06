# 🚀 Guia de Instalação do Ollama

## Passo 1: Instalar o Ollama

### Windows:
1. **Baixe o instalador:**
   - Acesse: https://ollama.ai/download
   - Baixe o instalador para Windows
   - Execute o arquivo `.exe` baixado

2. **Ou use o PowerShell:**
   ```powershell
   # Baixe usando winget (se disponível)
   winget install Ollama.Ollama
   
   # Ou use o instalador direto
   # Baixe de: https://ollama.ai/download/windows
   ```

## Passo 2: Verificar Instalação

Abra um novo terminal PowerShell e execute:

```powershell
ollama --version
```

Se aparecer a versão, está instalado corretamente!

## Passo 3: Baixar um Modelo

Escolha um modelo (recomendamos `llama3.2` por ser rápido e eficiente):

```powershell
ollama pull llama3.2
```

**Outros modelos disponíveis:**
- `llama3.2` - Recomendado (rápido e bom)
- `mistral` - Alternativa leve
- `codellama` - Focado em código (maior, mas melhor para análise de dados)

**Tempo estimado:** 5-15 minutos dependendo da sua internet

## Passo 4: Iniciar o Servidor Ollama

O Ollama precisa estar rodando para funcionar. Você tem duas opções:

### Opção A: Iniciar manualmente (recomendado para teste)
```powershell
ollama serve
```
**Deixe este terminal aberto!** O servidor precisa estar rodando.

### Opção B: Executar como serviço (Windows)
O Ollama geralmente inicia automaticamente como serviço no Windows após a instalação.

**Verificar se está rodando:**
```powershell
# Teste se o servidor está respondendo
curl http://localhost:11434/api/tags
```

## Passo 5: Testar o Modelo

```powershell
ollama run llama3.2 "Olá, como você está?"
```

Se responder, está tudo funcionando! ✅

## Passo 6: Configurar o Chatbot

O arquivo `.env` já foi configurado com:
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

## Passo 7: Instalar Dependências Python

```powershell
pip install langchain-community
```

Ou instale todas as dependências:
```powershell
pip install -r requirements.txt
```

## Passo 8: Reiniciar o Streamlit

1. Pare o Streamlit (Ctrl+C)
2. Inicie novamente:
```powershell
streamlit run app.py
```

## ✅ Pronto!

Agora seu chatbot está usando Ollama 100% gratuito!

## 🔧 Solução de Problemas

### Erro: "Connection refused"
- Certifique-se de que o Ollama está rodando: `ollama serve`
- Verifique se a porta 11434 está livre

### Erro: "Model not found"
- Baixe o modelo: `ollama pull llama3.2`
- Verifique se o nome do modelo no `.env` está correto

### Ollama não inicia
- Reinicie o computador após a instalação
- Verifique se há antivírus bloqueando
- Tente executar como administrador

## 📚 Mais Informações

- Site oficial: https://ollama.ai/
- Documentação: https://github.com/ollama/ollama
- Modelos disponíveis: https://ollama.ai/library

