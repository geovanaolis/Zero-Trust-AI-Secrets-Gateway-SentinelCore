from src.domain.sanitizer import PromptSanitizer

prompt_malicioso_ou_descuidado = """
Olá IA, resuma o contrato do cliente joao.silva@empresa.com.br.
O CPF dele é 123.456.789-00 e lembre-se de usar minha chave 
da OpenAI sk-1234567890abcdef1234567890abcdef12345678 para as tarefas.
"""

resultado = PromptSanitizer.sanitize(prompt_malicioso_ou_descuidado)

print("--- PROMPT ORIGINAL ---")
print(prompt_malicioso_ou_descuidado)
print("\n--- PROMPT SANITIZADO ---")
print(resultado)