# 🔑 Como Obter a API Key do Google Gemini (GRATUITO)

## Passo a Passo Rápido

### 1. Acesse o Google AI Studio
👉 **https://makersuite.google.com/app/apikey**

### 2. Faça Login
- Use sua conta Google (Gmail)
- Não precisa de conta empresarial, qualquer conta Google funciona

### 3. Crie uma Nova API Key
- Clique em **"Create API Key"** ou **"Criar chave de API"**
- Escolha um projeto (pode criar um novo se necessário)
- A chave será gerada automaticamente

### 4. Copie a Chave
- **IMPORTANTE:** Copie a chave imediatamente, ela só aparece uma vez!
- A chave começa com: `AIza...`

### 5. Adicione no Arquivo `.env`
Abra o arquivo `.env` e adicione:
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=AIza...sua_chave_aqui
```

### 6. Reinicie o Streamlit
```powershell
# Pare o Streamlit (Ctrl+C) e reinicie
streamlit run app.py
```

## ✅ Pronto!

Agora você está usando Google Gemini 100% gratuito!

## 💡 Limites Gratuitos

- **60 requisições por minuto**
- **1.500 requisições por dia**
- **32.000 tokens por minuto**

Isso é mais que suficiente para uso pessoal/testes!

## 🔒 Segurança

- **NUNCA** compartilhe sua API key publicamente
- Não commite o arquivo `.env` no Git
- Se perder a chave, gere uma nova

## 📚 Mais Informações

- Documentação: https://ai.google.dev/docs
- Limites: https://ai.google.dev/pricing
- Suporte: https://ai.google.dev/support

