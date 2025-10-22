import logging
import random
import re
from difflib import SequenceMatcher
import json

# Configura o logging para depuração
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Sistema de respostas inteligentes carregado com sucesso.")

# Limite do histórico para manter o contexto controlado
MAX_CONTEXT_LENGTH = 1000

# Base de conhecimento específica para governança de dados
BASE_CONHECIMENTO = {
    "lgpd": {
        "palavras_chave": ["lgpd", "lei geral de proteção", "proteção de dados", "privacidade", "consentimento"],
        "respostas": [
            "A LGPD (Lei Geral de Proteção de Dados) estabelece regras sobre coleta, armazenamento e uso de dados pessoais. Principais pontos: consentimento explícito, finalidade específica, minimização de dados e direito ao esquecimento.",
            "Para compliance com LGPD: mapeie todos os dados pessoais, implemente controles de acesso, documente finalidades, obtenha consentimento válido e estabeleça processo de resposta a incidentes.",
            "LGPD exige: registro de atividades de tratamento, análise de impacto à proteção de dados (AIPD), nomeação de encarregado de dados e políticas de privacidade claras."
        ]
    },
    "qualidade_dados": {
        "palavras_chave": ["qualidade", "duplicado", "inconsistente", "completo", "preciso", "atualizado", "limpeza"],
        "respostas": [
            "Qualidade de dados envolve: precisão (dados corretos), completude (sem campos vazios), consistência (formato padronizado), atualidade (dados recentes) e validade (conformidade com regras).",
            "Para melhorar qualidade: implemente validação na entrada, regras de negócio claras, monitoramento contínuo, processos de limpeza e padronização de formatos.",
            "Indicadores de qualidade: taxa de duplicação <5%, completude >95%, precisão >98%, tempo de atualização <24h e conformidade com padrões estabelecidos."
        ]
    },
    "seguranca": {
        "palavras_chave": ["segurança", "seguranca", "acesso", "criptografia", "auditoria", "controle", "permissões", "permissões", "proteção", "protecao"],
        "respostas": [
            "Segurança de dados requer: classificação por sensibilidade, controle de acesso baseado em roles (RBAC), criptografia em trânsito e repouso, monitoramento e auditoria contínua.",
            "Implemente: autenticação multifator, princípio do menor privilégio, logs de auditoria detalhados, backup seguro e plano de resposta a incidentes.",
            "Controles essenciais: firewalls, antivírus, patches de segurança, treinamento da equipe e testes de penetração regulares."
        ]
    },
    "governanca": {
        "palavras_chave": ["governança", "governanca", "política", "politica", "framework", "estrutura", "responsabilidade", "processo", "implementar", "implementação"],
        "respostas": [
            "Governança de dados inclui: estrutura organizacional (comitê, responsáveis), políticas e procedimentos, tecnologias de suporte e métricas de monitoramento.",
            "Framework de governança: defina responsabilidades (data owner, steward, custodian), estabeleça políticas claras, implemente controles e monitore compliance.",
            "Elementos essenciais: catálogo de dados, linhagem de dados, classificação, qualidade, segurança e lifecycle management."
        ]
    },
    "compliance": {
        "palavras_chave": ["compliance", "auditoria", "regulamentação", "conformidade", "norma"],
        "respostas": [
            "Compliance requer: documentação completa de processos, controles internos efetivos, auditorias regulares, treinamento contínuo e correção de não-conformidades.",
            "Para auditoria: mantenha logs detalhados, documente políticas, implemente controles de acesso, monitore atividades e prepare evidências de conformidade.",
            "Regulamentações importantes: LGPD, GDPR, SOX, Basel III. Cada uma tem requisitos específicos de documentação, controles e monitoramento."
        ]
    },
    "catalogacao": {
        "palavras_chave": ["catálogo", "catalogação", "inventário", "metadados", "linhagem", "mapeamento"],
        "respostas": [
            "Catálogo de dados deve incluir: nome, descrição, tipo, formato, localização, proprietário, qualidade, uso e linhagem de cada ativo de dados.",
            "Metadados essenciais: técnicos (tipo, tamanho, formato), de negócio (significado, uso), operacionais (frequência de atualização) e de qualidade (completude, precisão).",
            "Linhagem de dados mostra: origem, transformações, destino e dependências. Fundamental para auditoria, debugging e impacto de mudanças."
        ]
    }
}

def limpar_contexto(contexto):
    """Garante que o histórico de contexto não ultrapasse o limite."""
    return contexto[-MAX_CONTEXT_LENGTH:] if len(contexto) > MAX_CONTEXT_LENGTH else contexto

def calcular_similaridade(texto1, texto2):
    """Calcula a similaridade entre dois textos usando SequenceMatcher."""
    return SequenceMatcher(None, texto1.lower(), texto2.lower()).ratio()

def encontrar_topicos_relevantes(mensagem):
    """Encontra tópicos relevantes na mensagem usando busca semântica."""
    mensagem_lower = mensagem.lower()
    topicos_encontrados = []
    
    for topico, info in BASE_CONHECIMENTO.items():
        for palavra_chave in info["palavras_chave"]:
            # Busca exata
            if palavra_chave in mensagem_lower:
                topicos_encontrados.append((topico, 1.0))
                break
            # Busca por similaridade
            elif calcular_similaridade(mensagem_lower, palavra_chave) > 0.6:
                topicos_encontrados.append((topico, calcular_similaridade(mensagem_lower, palavra_chave)))
                break
    
    # Remove duplicatas e ordena por relevância
    topicos_unicos = {}
    for topico, score in topicos_encontrados:
        if topico not in topicos_unicos or score > topicos_unicos[topico]:
            topicos_unicos[topico] = score
    
    return sorted(topicos_unicos.items(), key=lambda x: x[1], reverse=True)

def extrair_intencao(mensagem):
    """Extrai a intenção da mensagem do usuário."""
    mensagem_lower = mensagem.lower()
    
    # Padrões de intenção
    intencoes = {
        "saudacao": ["ola", "oi", "hello", "hi", "bom dia", "boa tarde", "boa noite", "e aí", "eai"],
        "pergunta": ["como", "what", "quando", "onde", "por que", "porque", "qual", "quais", "?"],
        "explicacao": ["explicar", "explica", "o que é", "definir", "significa", "conceito"],
        "procedimento": ["como fazer", "passo a passo", "processo", "implementar", "aplicar", "executar"],
        "problema": ["problema", "erro", "falha", "não funciona", "nao funciona", "dificuldade", "dúvida"],
        "despedida": ["tchau", "bye", "até logo", "obrigado", "obrigada", "valeu", "obrigado", "obrigada"],
        "ajuda": ["ajuda", "help", "dúvida", "duvida", "não sei", "nao sei", "socorro"]
    }
    
    for intencao, palavras in intencoes.items():
        if any(palavra in mensagem_lower for palavra in palavras):
            return intencao
    
    return "geral"

def gerar_resposta_contextual(mensagem, contexto=""):
    """Gera resposta baseada no contexto da conversa."""
    # Analisa o contexto para entender melhor a conversa
    if contexto:
        contexto_lower = contexto.lower()
        # Se há menção a LGPD no contexto, prioriza respostas sobre LGPD
        if "lgpd" in contexto_lower:
            return "Continuando sobre LGPD, posso esclarecer outros aspectos específicos. O que gostaria de saber?"
        elif "qualidade" in contexto_lower:
            return "Sobre qualidade de dados, posso detalhar outros aspectos. Qual sua dúvida específica?"
    
    return None

def gerar_resposta(mensagem, contexto=''):
    """Gera uma resposta inteligente baseada em análise semântica e contexto."""
    
    logging.info(f"Processando mensagem: {mensagem}")
    
    try:
        # Primeiro, tenta resposta contextual
        resposta_contextual = gerar_resposta_contextual(mensagem, contexto)
        if resposta_contextual:
            novo_contexto = f"{limpar_contexto(contexto)}\nUsuário: {mensagem}\nChat Governança: {resposta_contextual}\n"
            logging.info(f"Resposta contextual gerada: {resposta_contextual}")
            return resposta_contextual, novo_contexto
        
        # Extrai intenção da mensagem
        intencao = extrair_intencao(mensagem)
        logging.info(f"Intenção detectada: {intencao}")
        
        # Encontra tópicos relevantes
        topicos = encontrar_topicos_relevantes(mensagem)
        logging.info(f"Tópicos encontrados: {topicos}")
        
        # Gera resposta baseada na intenção e tópicos
        resposta_final = gerar_resposta_inteligente_v2(mensagem, intencao, topicos)

        # Atualiza o contexto para a próxima rodada
        novo_contexto = f"{limpar_contexto(contexto)}\nUsuário: {mensagem}\nChat Governança: {resposta_final}\n"

        logging.info(f"Resposta gerada: {resposta_final}")
        return resposta_final, novo_contexto

    except Exception as e:
        logging.error(f"Erro ao gerar resposta: {e}")
        # Fallback para resposta básica
        resposta_fallback = "Desculpe, ocorreu um problema. Tente reformular sua pergunta."
        return resposta_fallback, contexto

def gerar_resposta_inteligente_v2(mensagem, intencao, topicos):
    """Gera respostas inteligentes usando análise semântica avançada."""
    mensagem_lower = mensagem.lower().strip()
    
    # Respostas baseadas na intenção
    if intencao == "saudacao":
        saudacoes = [
            "Olá! Sou o Chat Governança, especializado em governança de dados. Como posso ajudá-lo hoje?",
            "Oi! Estou aqui para auxiliar com questões de dados, políticas e compliance. Em que posso ser útil?",
            "Bom dia! Sou especialista em governança de dados. Qual sua necessidade específica?",
            "Olá! Posso ajudar com LGPD, qualidade de dados, segurança e compliance. O que gostaria de saber?"
        ]
        return random.choice(saudacoes)
    
    elif intencao == "despedida":
        despedidas = [
            "Foi um prazer ajudar! Estou sempre disponível para questões de governança de dados.",
            "De nada! Volte sempre que precisar de auxílio com dados e compliance.",
            "Por nada! Qualquer dúvida sobre governança de dados, estou aqui.",
            "Disponha! Estou sempre pronto para auxiliar com políticas e qualidade de dados."
        ]
        return random.choice(despedidas)
    
    elif intencao == "ajuda":
        respostas_ajuda = [
            "Posso ajudar com: LGPD, qualidade de dados, segurança, compliance, catálogo de dados e políticas. Seja específico na sua pergunta para melhor atendimento.",
            "Sou especialista em governança de dados. Faça perguntas sobre: políticas, qualidade, segurança, LGPD ou compliance.",
            "Posso auxiliar em: classificação de dados, controle de acesso, qualidade, compliance e regulamentações. Qual sua necessidade específica?",
            "Estou aqui para ajudar com governança de dados. Para melhor atendimento, seja específico sobre sua dúvida."
        ]
        return random.choice(respostas_ajuda)
    
    # Respostas baseadas nos tópicos encontrados
    if topicos:
        topico_principal = topicos[0][0]
        score = topicos[0][1]
        
        if score > 0.7:  # Alta confiança
            respostas = BASE_CONHECIMENTO[topico_principal]["respostas"]
            resposta_base = random.choice(respostas)
            
            # Personaliza baseada na intenção
            if intencao == "explicacao":
                return f"Vou explicar sobre {topico_principal.replace('_', ' ')}: {resposta_base}"
            elif intencao == "procedimento":
                return f"Para implementar {topico_principal.replace('_', ' ')}: {resposta_base}"
            elif intencao == "pergunta":
                return f"Sobre {topico_principal.replace('_', ' ')}: {resposta_base}"
            else:
                return resposta_base
    
    # Respostas específicas para perguntas comuns
    if any(palavra in mensagem_lower for palavra in ['o que é', 'definir', 'significa']):
        if any(palavra in mensagem_lower for palavra in ['lgpd', 'lei geral']):
            return "LGPD é a Lei Geral de Proteção de Dados (Lei 13.709/2018) que estabelece regras sobre coleta, armazenamento e uso de dados pessoais no Brasil. Principais pontos: consentimento explícito, finalidade específica, minimização de dados e direito ao esquecimento."
        elif any(palavra in mensagem_lower for palavra in ['governança', 'governanca']):
            return "Governança de dados é o conjunto de políticas, processos e tecnologias que garantem o uso adequado, seguro e eficiente dos dados organizacionais. Inclui: estrutura organizacional, políticas claras, controles de qualidade e segurança."
        elif any(palavra in mensagem_lower for palavra in ['qualidade']):
            return "Qualidade de dados refere-se à precisão, completude, consistência e atualidade das informações. Envolve: validação na entrada, limpeza de dados, padronização e monitoramento contínuo."
    
    elif any(palavra in mensagem_lower for palavra in ['como implementar', 'como fazer', 'passo a passo', 'implementar']):
        if any(palavra in mensagem_lower for palavra in ['lgpd']):
            return "Para implementar LGPD: 1) Mapeie todos os dados pessoais, 2) Classifique por sensibilidade, 3) Documente finalidades, 4) Implemente controles de acesso, 5) Estabeleça processo de resposta a incidentes, 6) Treine a equipe."
        elif any(palavra in mensagem_lower for palavra in ['governança', 'governanca']):
            return "Para implementar governança: 1) Crie comitê de dados, 2) Defina responsabilidades (owner, steward), 3) Estabeleça políticas, 4) Implemente catálogo de dados, 5) Monitore compliance, 6) Treine equipes."
    
    # Melhorar detecção de perguntas sobre governança
    elif any(palavra in mensagem_lower for palavra in ['governança', 'governanca']) and intencao == "explicacao":
        return "Governança de dados é o conjunto de políticas, processos e tecnologias que garantem o uso adequado, seguro e eficiente dos dados organizacionais. Inclui: estrutura organizacional, políticas claras, controles de qualidade e segurança."
    
    # Resposta padrão inteligente
    respostas_padrao = [
        "Interessante pergunta! Posso ajudar melhor se você for mais específico sobre governança de dados, LGPD, qualidade ou segurança.",
        "Entendi sua mensagem. Para melhor atendimento, seja mais específico sobre sua necessidade em governança de dados.",
        "Posso ajudar com governança de dados, LGPD, qualidade, segurança ou compliance. Qual sua dúvida específica?",
        "Sou especialista em governança de dados. Como posso ser mais útil para você? Seja específico na sua pergunta.",
        "Para melhor atendimento, faça perguntas mais específicas sobre dados, políticas ou compliance."
    ]
    return random.choice(respostas_padrao)

def gerar_resposta_fallback(mensagem):
    """Fallback para casos de erro - usa o sistema inteligente."""
    intencao = extrair_intencao(mensagem)
    topicos = encontrar_topicos_relevantes(mensagem)
    return gerar_resposta_inteligente_v2(mensagem, intencao, topicos)

# Execução local para testes no terminal
if __name__ == "__main__":
    contexto = ""
    print("Chat Governança ativo! Digite sua mensagem. (digite 'sair' para encerrar)")
    while True:
        user_msg = input("Você: ")
        if user_msg.lower().strip() in ["sair", "exit", "fim"]:
            print("Chat Governança: Encerrando sessão. Até logo!")
            break
        resposta, contexto = gerar_resposta(user_msg, contexto)
        print(f"Chat Governança: {resposta}")