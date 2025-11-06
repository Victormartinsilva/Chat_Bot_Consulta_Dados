# 🔧 Configurar Secrets e CSV no Streamlit Cloud

Este guia mostra passo a passo como configurar os Secrets e fazer upload do CSV no Streamlit Cloud.

## 📋 Passo 1: Configurar os Secrets

1. **Acesse seu app no Streamlit Cloud:**
   - Vá para: https://share.streamlit.io/
   - Faça login com sua conta GitHub
   - Clique no seu app: `Chat_Bot_Consulta_Dados`

2. **Abra as configurações:**
   - Clique no menu **"☰"** (três linhas) no canto superior direito
   - Clique em **"Settings"**

3. **Configure os Secrets:**
   - No menu lateral, clique em **"Secrets"**
   - Cole o seguinte conteúdo na caixa de texto:

```toml
LLM_PROVIDER = "gemini"
GOOGLE_API_KEY = "AIzaSyAZjyQKeGSOseQKJ-JeLQ0jnQIq-DcFmBA"
GEMINI_MODEL = "gemini-2.5-flash"
```

4. **Salve:**
   - Clique em **"Save"** no final da página
   - Aguarde a confirmação

## 📁 Passo 2: Fazer Upload do CSV

### Opção A: Upload Manual (Recomendado)

1. **Acesse a seção de arquivos:**
   - No menu lateral de Settings, clique em **"Files"**
   - Ou acesse diretamente: `https://share.streamlit.io/[seu-usuario]/[seu-app]/settings/files`

2. **Faça upload do arquivo:**
   - Clique em **"Upload file"** ou arraste o arquivo para a área indicada
   - Selecione o arquivo `data.csv` do seu computador
   - Aguarde o upload completar

3. **Verifique:**
   - O arquivo deve aparecer na lista de arquivos
   - Certifique-se de que o nome é exatamente `data.csv`

### Opção B: Usar URL do CSV (Alternativa)

Se preferir hospedar o CSV em outro lugar:

1. **Faça upload do CSV em um serviço de hospedagem:**
   - Google Drive (compartilhar como link público)
   - Dropbox (link direto)
   - GitHub (raw file)
   - Qualquer serviço que forneça link direto para download

2. **Adicione a URL nos Secrets:**
   - Volte para **Settings → Secrets**
   - Adicione a linha:
   ```toml
   CSV_URL = "https://exemplo.com/dados.csv"
   ```

## 🔄 Passo 3: Reiniciar o App

Após configurar os Secrets e fazer upload do CSV:

1. **Volte para a página principal do app**
2. **Clique no menu "☰" → "Redeploy"**
   - Ou simplesmente aguarde alguns segundos - o app detecta mudanças automaticamente

## ✅ Verificação

Após o redeploy, verifique se:

- ✅ O app carrega sem erros
- ✅ A mensagem mostra: "✅ CSV carregado do arquivo local: data.csv"
- ✅ O DataFrame é exibido corretamente
- ✅ O provedor LLM mostra: "🔧 Provedor LLM configurado: **GEMINI**"

## 🐛 Solução de Problemas

### Erro: "Arquivo CSV não encontrado"

**Solução:**
1. Verifique se o arquivo foi feito upload corretamente em Settings → Files
2. Certifique-se de que o nome do arquivo é exatamente `data.csv` (case-sensitive)
3. Aguarde alguns segundos após o upload para o arquivo estar disponível

### Erro: "GOOGLE_API_KEY não encontrada"

**Solução:**
1. Verifique se os Secrets foram salvos corretamente
2. Certifique-se de que não há espaços extras nas chaves
3. Verifique se a API key está correta

### App não atualiza após mudanças

**Solução:**
1. Clique em "Redeploy" no menu do app
2. Ou faça um pequeno commit no GitHub para forçar o redeploy

## 📝 Formato Correto dos Secrets

Certifique-se de que os Secrets estão no formato TOML correto:

```toml
# ✅ CORRETO
LLM_PROVIDER = "gemini"
GOOGLE_API_KEY = "AIzaSyAZjyQKeGSOseQKJ-JeLQ0jnQIq-DcFmBA"
GEMINI_MODEL = "gemini-2.5-flash"

# ❌ ERRADO (não use aspas simples ou espaços extras)
LLM_PROVIDER = 'gemini'
GOOGLE_API_KEY = " AIzaSyAZjyQKeGSOseQKJ-JeLQ0jnQIq-DcFmBA "
```

## 🎉 Pronto!

Após seguir estes passos, seu app deve estar funcionando perfeitamente no Streamlit Cloud!

