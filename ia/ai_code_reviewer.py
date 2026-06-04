import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

# ==========================================
# 🧠 MICRO AI CODE REVIEWER
# ==========================================
# Um agente inteligente de terminal para revisar código.

def setup_ai():
    """Carrega as variáveis de ambiente e configura a API do Gemini."""
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERRO: A chave da API não foi encontrada.")
        print("Crie um arquivo .env na mesma pasta e adicione: GEMINI_API_KEY=sua_chave_aqui")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    
    # Usando o modelo mais recente de texto
    return genai.GenerativeModel('gemini-1.5-pro-latest')

def read_code_file(filepath: str) -> str:
    """Lê o conteúdo do arquivo de código passado pelo usuário."""
    if not os.path.exists(filepath):
        print(f"❌ ERRO: O arquivo '{filepath}' não foi encontrado.")
        sys.exit(1)
        
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def review_code(model, code: str):
    """Envia o código para o Gemini analisar e imprimir o resultado."""
    print("🤖 Analisando o seu código... Aguarde.")
    
    prompt = f"""
    Você é um Engenheiro de Software Sênior especializado em Clean Code, Segurança e Performance.
    Sua tarefa é fazer um Code Review detalhado do código abaixo.
    
    Por favor, retorne sua análise com os seguintes tópicos (usando Markdown):
    1. **Visão Geral**: O que o código faz (resumo rápido).
    2. **Pontos Positivos**: O que está bem feito.
    3. **Melhorias de Refatoração / Clean Code**: Sugestões de legibilidade.
    4. **Segurança e Bugs**: Algum risco crítico? Se não, diga que parece seguro.
    
    Código a ser analisado:
    ```
    {code}
    ```
    """
    
    try:
        response = model.generate_content(prompt)
        print("\n" + "="*50)
        print("✨ RESULTADO DO CODE REVIEW ✨")
        print("="*50 + "\n")
        print(response.text)
    except Exception as e:
        print(f"❌ Erro ao comunicar com a IA: {e}")

def main():
    if len(sys.argv) < 2:
        print("Uso correto: python ai_code_reviewer.py <caminho_do_arquivo>")
        print("Exemplo: python ai_code_reviewer.py meu_script.py")
        sys.exit(1)
        
    target_file = sys.argv[1]
    code_content = read_code_file(target_file)
    
    model = setup_ai()
    review_code(model, code_content)

if __name__ == "__main__":
    main()
