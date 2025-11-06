# 🚀 Guia de Deploy no Streamlit Cloud

Este guia irá ajudá-lo a fazer o deploy do Chatbot de Consulta de Dados no Streamlit Cloud.

## ✅ Pré-requisitos

- ✅ Repositório no GitHub: https://github.com/Victormartinsilva/Chat_Bot_Consulta_Dados
- ✅ Conta no Streamlit Cloud: https://share.streamlit.io
- ✅ API Key do Google Gemini (ou outro provedor LLM)

## 📋 Passo a Passo

### 1. Acesse o Streamlit Cloud

1. Vá para: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Clique em **"New app"**

### 2. Configure o Repositório

Preencha os campos:

- **Repository:** `Victormartinsilva/Chat_Bot_Consulta_Dados`
- **Branch:** `main`
- **Main file path:** `Chat_Bot/Chat_Bot/app.py`
- **Python version:** `3.11` (ou deixe em branco para usar a padrão)

### 3. Configure os Secrets

Clique em **"Advanced settings"** e depois em **"Secrets"**. Cole o seguinte conteúdo:

```toml
LLM_PROVIDER = "gemini"
GOOGLE_API_KEY = "AIzaSyAZjyQKeGSOseQKJ-JeLQ0jnQIq-DcFmBA"
GEMINI_MODEL = "gemini-2.5-flash"
```

**⚠️ IMPORTANTE:** Substitua `AIzaSyAZjyQKeGSOseQKJ-JeLQ0jnQIq-DcFmBA` pela sua própria API key do Gemini.

### 4. Faça Upload do Arquivo CSV

Você tem duas opções:

#### Opção A: Upload Manual (Recomendado)

1. No Streamlit Cloud, vá em **"Settings"** → **"Files"**
2. Clique em **"Upload file"**
3. Faça upload do arquivo `data.csv`
4. O arquivo será salvo na raiz do projeto

#### Opção B: Usar URL do CSV

1. Faça upload do CSV em um serviço de hospedagem (Google Drive, Dropbox, etc.)
2. Obtenha o link direto para download
3. Adicione nos Secrets:
   ```toml
   CSV_URL = "https://exemplo.com/dados.csv"
   ```

### 5. Deploy!

1. Clique em **"Deploy!"**
2. Aguarde o build (pode levar alguns minutos na primeira vez)
3. Seu app estará disponível em: `https://seu-app-name.streamlit.app`

## 🔧 Solução de Problemas

### Erro: "Module not found"

- Verifique se todas as dependências estão no `requirements.txt`
- Certifique-se de que as versões são compatíveis

### Erro: "File not found: data.csv"

- Verifique se o arquivo foi feito upload corretamente
- Ou configure o `CSV_URL` nos Secrets

### Erro: "API Key not found"

- Verifique se os Secrets estão configurados corretamente
- Certifique-se de que não há espaços extras nas chaves

### Build muito lento

- O primeiro build pode levar 5-10 minutos
- Builds subsequentes são mais rápidos (cache)

## 📝 Checklist de Deploy

- [ ] Repositório no GitHub está atualizado
- [ ] Secrets configurados no Streamlit Cloud
- [ ] Arquivo CSV feito upload (ou URL configurada)
- [ ] Main file path correto: `Chat_Bot/Chat_Bot/app.py`
- [ ] Python version: 3.11
- [ ] Deploy iniciado e build concluído com sucesso

## 🎉 Pronto!

Após o deploy, seu chatbot estará disponível publicamente e poderá ser acessado de qualquer lugar!

## 🔗 Links Úteis

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Google Gemini API](https://makersuite.google.com/app/apikey)

