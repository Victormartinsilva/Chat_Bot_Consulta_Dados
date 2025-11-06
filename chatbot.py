import os
import pandas as pd
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# O nome do arquivo CSV foi padronizado para 'data.csv' na fase 1
CSV_FILE_PATH = "data.csv"

# Configuração do provedor LLM (openai, ollama, gemini)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()

def criar_llm():
    """
    Cria e retorna o LLM baseado no provedor configurado.
    Suporta: OpenAI, Ollama (gratuito/local), Google Gemini (gratuito)
    """
    if LLM_PROVIDER == "ollama":
        try:
            from langchain_community.llms import Ollama
            model_name = os.getenv("OLLAMA_MODEL", "llama3.2")  # Modelo padrão
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            print(f"Usando Ollama com modelo: {model_name}")
            # Ollama usa LLM (não ChatLLM) para compatibilidade com create_pandas_dataframe_agent
            return Ollama(model=model_name, base_url=base_url, temperature=0)
        except ImportError:
            raise ImportError("Para usar Ollama, instale: pip install langchain-community")
        except Exception as e:
            raise Exception(f"Erro ao conectar com Ollama. Certifique-se de que o Ollama está rodando em {base_url}. Erro: {e}")
    
    elif LLM_PROVIDER == "gemini":
        try:
            # Usa google-generativeai diretamente com wrapper customizado
            from langchain_core.language_models.llms import LLM
            from langchain_core.callbacks.manager import CallbackManagerForLLMRun
            from typing import Optional, List, Any
            import google.generativeai as genai
            
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
            
            model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
            
            # Configura o Google Generative AI
            genai.configure(api_key=api_key)
            
            print(f"Usando Google Gemini com modelo: {model_name}")
            
            # Cria um wrapper LLM customizado para compatibilidade com LangChain
            class GeminiLLM(LLM):
                gemini_model_name: str = ""
                gemini_api_key: str = ""
                model: Any = None
                
                def __init__(self, gemini_model_name: str = "", gemini_api_key: str = "", **kwargs):
                    # Remove os parâmetros customizados antes de passar para super()
                    filtered_kwargs = {k: v for k, v in kwargs.items() if k not in ['gemini_model_name', 'gemini_api_key']}
                    super().__init__(**filtered_kwargs)
                    
                    # Define os valores do modelo e API key
                    self.gemini_model_name = gemini_model_name or model_name
                    self.gemini_api_key = gemini_api_key or api_key
                    
                    # Configura e cria o modelo
                    genai.configure(api_key=self.gemini_api_key)
                    try:
                        self.model = genai.GenerativeModel(self.gemini_model_name)
                    except Exception as e:
                        # Se falhar, tenta listar modelos disponíveis
                        try:
                            available = [m.name.replace('models/', '') for m in genai.list_models() 
                                        if 'generateContent' in m.supported_generation_methods]
                            raise Exception(
                                f"Modelo '{self.gemini_model_name}' não encontrado. "
                                f"Modelos disponíveis: {', '.join(available[:5])}"
                            )
                        except:
                            raise Exception(f"Erro ao criar modelo '{self.gemini_model_name}': {e}")
                
                @property
                def _llm_type(self) -> str:
                    return "gemini"
                
                def _call(
                    self,
                    prompt: str,
                    stop: Optional[List[str]] = None,
                    run_manager: Optional[CallbackManagerForLLMRun] = None,
                    **kwargs: Any,
                ) -> str:
                    try:
                        # Configura parâmetros de geração
                        generation_config = genai.types.GenerationConfig(
                            temperature=0,
                            max_output_tokens=4096,
                            top_p=0.95,
                            top_k=40
                        )
                        
                        response = self.model.generate_content(
                            prompt,
                            generation_config=generation_config
                        )
                        
                        # Extrai o texto da resposta de forma mais robusta
                        text = None
                        
                        # Tenta diferentes formas de extrair o texto
                        if hasattr(response, 'text') and response.text:
                            text = response.text
                        elif hasattr(response, 'candidates') and response.candidates:
                            if len(response.candidates) > 0:
                                candidate = response.candidates[0]
                                if hasattr(candidate, 'content') and candidate.content:
                                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                                        if len(candidate.content.parts) > 0:
                                            text = candidate.content.parts[0].text
                                    elif hasattr(candidate.content, 'text'):
                                        text = candidate.content.text
                        elif hasattr(response, 'parts') and response.parts:
                            if len(response.parts) > 0:
                                text = response.parts[0].text
                        
                        # Se não conseguiu extrair, tenta converter para string
                        if not text:
                            text = str(response)
                        
                        # Limpa a resposta removendo caracteres problemáticos
                        if text:
                            text = text.strip()
                            # Remove possíveis prefixos/sufixos indesejados
                            if text.startswith("```"):
                                # Remove blocos de código markdown se não for necessário
                                pass
                        
                        return text if text else "Resposta vazia do modelo."
                    except Exception as e:
                        error_msg = str(e)
                        # Se o modelo não for encontrado, sugere modelos disponíveis
                        if "404" in error_msg or "não foi encontrado" in error_msg.lower() or "not found" in error_msg.lower():
                            try:
                                genai.configure(api_key=self.gemini_api_key)
                                available_models = [m.name.replace('models/', '') for m in genai.list_models() 
                                                   if 'generateContent' in m.supported_generation_methods]
                                raise Exception(
                                    f"Modelo '{self.gemini_model_name}' não encontrado. "
                                    f"Modelos disponíveis: {', '.join(available_models[:5])}. "
                                    f"Atualize GEMINI_MODEL no arquivo .env"
                                )
                            except Exception as inner_e:
                                if "Modelo" in str(inner_e):
                                    raise inner_e
                                raise Exception(
                                    f"Modelo '{self.gemini_model_name}' não encontrado. "
                                    f"Tente usar: gemini-2.5-flash, gemini-2.0-flash, ou gemini-2.5-pro"
                                )
                        raise
            
            return GeminiLLM(gemini_model_name=model_name, gemini_api_key=api_key)
            
        except ImportError as e:
            raise ImportError(f"Para usar Gemini, instale: pip install google-generativeai. Erro: {e}")
        except Exception as e:
            raise Exception(f"Erro ao inicializar Gemini: {e}")
    
    else:  # OpenAI (padrão)
        try:
            from langchain_openai import ChatOpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY não encontrada no arquivo .env")
            model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            print(f"Usando OpenAI com modelo: {model_name}")
            return ChatOpenAI(model=model_name, temperature=0)
        except ImportError:
            raise ImportError("Para usar OpenAI, instale: pip install langchain-openai")
        except Exception as e:
            raise Exception(f"Erro ao inicializar OpenAI: {e}")

def criar_agente_pandas():
    """
    Cria e retorna o agente LangChain para consultas em DataFrame Pandas.
    """
    try:
        # 1. Carregar o DataFrame
        df = pd.read_csv(CSV_FILE_PATH)
        
        # 2. Inicializar o LLM baseado no provedor configurado
        llm = criar_llm()
        
        # 3. Criar o agente Pandas
        # O agente utiliza o LLM e o DataFrame para responder perguntas.
        # verbose=True é importante para mostrar o raciocínio (código Python gerado)
        agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            allow_dangerous_code=True,
            max_iterations=5,
            max_execution_time=60
        )
        
        return agent

    except FileNotFoundError:
        print(f"Erro: Arquivo CSV não encontrado em {CSV_FILE_PATH}")
        return None
    except Exception as e:
        print(f"Erro ao inicializar o agente: {e}")
        return None

# Inicializa o agente uma vez
pandas_agent = criar_agente_pandas()

def gerar_resposta(pergunta: str):
    """
    Recebe uma pergunta e retorna a resposta do agente e o raciocínio.
    
    Args:
        pergunta: A pergunta do usuário.
        
    Returns:
        Uma tupla (resposta, raciocínio).
    """
    if pandas_agent is None:
        return "O agente não pôde ser inicializado. Verifique o arquivo CSV e a chave da API.", ""

    # O LangChain executa a cadeia e retorna o resultado.
    # Para obter o raciocínio (código Python gerado), precisamos inspecionar a saída
    # do `verbose=True` ou usar um callback. Como o `create_pandas_dataframe_agent`
    # é uma abstração, vamos focar na resposta final e instruir o LLM a incluir
    # o raciocínio na resposta.
    
    # Adicionamos uma instrução ao prompt para que o agente inclua o código Python
    # que ele usou para chegar à resposta.
    prompt_com_instrucao = (
        f"{pergunta}\n\n"
        "IMPORTANTE: Depois de responder à pergunta, inclua o código Python completo "
        "que você gerou e executou para obter a resposta, formatado em um bloco de código "
        "Markdown (```python...```). Se a resposta for trivial e não envolver código, "
        "apenas responda à pergunta."
    )
    
    try:
        # A chamada `agent.invoke` retorna um dicionário com a chave 'output'
        response = pandas_agent.invoke({"input": prompt_com_instrucao})
        
        # Extrai a resposta do output
        resposta_completa = response.get("output", "Não foi possível obter uma resposta.")
        
        # Se houver intermediate_steps, tenta extrair o código executado
        raciocinio = ""
        if "intermediate_steps" in response:
            for step in response["intermediate_steps"]:
                if len(step) >= 2 and hasattr(step[0], 'tool_input'):
                    tool_input = step[0].tool_input
                    if isinstance(tool_input, str) and 'python' in tool_input.lower():
                        raciocinio += tool_input + "\n\n"
        
        # Tentativa de separar a resposta do código (raciocínio)
        # O código estará dentro de ```python...```
        import re
        match = re.search(r"```python\n(.*?)```", resposta_completa, re.DOTALL)
        
        if match:
            raciocinio = match.group(1).strip()
            # Remove o bloco de código da resposta final para o usuário
            resposta_final = resposta_completa.replace(match.group(0), "").strip()
        else:
            resposta_final = resposta_completa
            if not raciocinio:
                raciocinio = "O agente não forneceu o código Python para esta consulta."
            
        return resposta_final, raciocinio
        
    except Exception as e:
        error_msg = str(e)
        print(f"Erro durante a invocação do agente: {error_msg}")
        
        # Tratamento para erros de parsing - tenta extrair a resposta mesmo assim
        if "OUTPUT_PARSING_FAILURE" in error_msg or "parsing error" in error_msg.lower() or "parse-able action" in error_msg.lower() or "Parsing LLM output" in error_msg or "Could not parse LLM output" in error_msg:
            # Tenta extrair a resposta final do erro
            import re
            
            # Procura por "Final Answer:" na mensagem de erro
            final_answer_match = re.search(r"Final Answer:\s*(.+?)(?:\n\n|Resposta:|```|$)", error_msg, re.IGNORECASE | re.DOTALL)
            if not final_answer_match:
                # Tenta procurar por "Resposta:"
                final_answer_match = re.search(r"Resposta:\s*(.+?)(?:\n\n|```|$)", error_msg, re.IGNORECASE | re.DOTALL)
            
            # Se não encontrou "Final Answer" ou "Resposta", tenta extrair do output direto
            if not final_answer_match:
                # Procura por texto entre backticks (resposta do LLM)
                output_match = re.search(r"Could not parse LLM output: `(.+?)`", error_msg, re.DOTALL)
                if output_match:
                    resposta_final = output_match.group(1).strip()
                    # Se é uma resposta simples (saudação), retorna ela
                    if resposta_final and len(resposta_final) < 200:
                        return resposta_final, ""
            
            if final_answer_match:
                resposta_final = final_answer_match.group(1).strip()
                # Remove código markdown e informações técnicas
                resposta_final = re.sub(r'```python.*?```', '', resposta_final, flags=re.DOTALL).strip()
                resposta_final = re.sub(r'For troubleshooting.*', '', resposta_final, flags=re.DOTALL).strip()
                
                # Tenta extrair o código executado
                raciocinio = ""
                # Procura por "Action Input:" que contém o código
                action_input_match = re.search(r"Action Input:\s*(.+?)(?:\n|Observation:|Thought:|$)", error_msg, re.DOTALL)
                if action_input_match:
                    raciocinio = action_input_match.group(1).strip()
                else:
                    # Tenta extrair de blocos de código markdown
                    code_match = re.search(r"```python\n(.*?)```", error_msg, re.DOTALL)
                    if code_match:
                        raciocinio = code_match.group(1).strip()
                    else:
                        raciocinio = ""
                
                return resposta_final, raciocinio
        
        # Tratamento específico para erros de quota da API
        if "429" in error_msg or "quota" in error_msg.lower() or "insufficient_quota" in error_msg.lower():
            mensagem = (
                "⚠️ **Erro de Quota da API OpenAI**\n\n"
                "A quota da sua conta OpenAI foi excedida.\n\n"
                "**💡 Soluções GRATUITAS:**\n\n"
                "1. **Ollama (100% Gratuito, roda localmente):**\n"
                "   - Instale: https://ollama.ai/\n"
                "   - Baixe um modelo: `ollama pull llama3.2`\n"
                "   - No arquivo `.env`, adicione: `LLM_PROVIDER=ollama`\n\n"
                "2. **Google Gemini (Gratuito):**\n"
                "   - Obtenha API key: https://makersuite.google.com/app/apikey\n"
                "   - No arquivo `.env`, adicione:\n"
                "     `LLM_PROVIDER=gemini`\n"
                "     `GOOGLE_API_KEY=sua_chave_aqui`\n\n"
                "**Ou resolva o problema da OpenAI:**\n"
                "- Verifique sua conta: https://platform.openai.com/account/billing\n"
                "- Adicione créditos ou aguarde o reset do limite"
            )
            return mensagem, ""
        
        # Tratamento para outros erros de API
        if "401" in error_msg or "authentication" in error_msg.lower() or "invalid" in error_msg.lower():
            mensagem = (
                "🔑 **Erro de Autenticação da API**\n\n"
                "A chave da API OpenAI é inválida ou expirou. Verifique:\n\n"
                "1. Se a chave no arquivo `.env` está correta\n"
                "2. Se a chave não expirou\n"
                "3. Se a chave tem permissões adequadas\n\n"
                "Gere uma nova chave em: https://platform.openai.com/api-keys"
            )
            return mensagem, ""
        
        # Erro genérico
        mensagem = (
            f"❌ **Erro ao processar sua pergunta**\n\n"
            f"Detalhes do erro: {error_msg}\n\n"
            "Por favor, tente novamente ou verifique sua conexão com a API da OpenAI."
        )
        return mensagem, ""

# Exemplo de uso (opcional, para testes rápidos)
if __name__ == "__main__":
    print("Agente Pandas inicializado. Testando...")
    # Certifique-se de que o arquivo 'data.csv' existe para este teste
    if os.path.exists(CSV_FILE_PATH):
        resposta, raciocinio = gerar_resposta("Quantas linhas e colunas o DataFrame possui?")
        print("\n--- Resposta ---")
        print(resposta)
        print("\n--- Raciocínio (Código Python) ---")
        print(raciocinio)
    else:
        print(f"O arquivo {CSV_FILE_PATH} não foi encontrado. Não é possível testar.")
