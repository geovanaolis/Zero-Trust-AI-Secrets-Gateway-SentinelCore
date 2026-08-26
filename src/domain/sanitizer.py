import re

class PromptSanitizer:
    """
    Serviço de Domínio responsável por varrer textos e ocultar 
    Informações Pessoalmente Identificáveis (PII) e Secrets.
    """
    
    # Expressões Regulares (Regex) para identificar padrões sensíveis
    CPF_PATTERN = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b' # Formato: 000.000.000-00
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    API_KEY_PATTERN = r'\b(sk-[a-zA-Z0-9]{32,})\b' # Padrão básico de chaves tipo OpenAI (sk-...)

    @classmethod
    def sanitize(cls, text: str) -> str:
        """
        Recebe um texto puro (prompt) e retorna o texto sanitizado.
        """
        if not text:
            return text
            
        # Aplica as substituições mascarando os dados
        sanitized = re.sub(cls.CPF_PATTERN, '[CPF_MASCARADO]', text)
        sanitized = re.sub(cls.EMAIL_PATTERN, '[EMAIL_MASCARADO]', sanitized)
        sanitized = re.sub(cls.API_KEY_PATTERN, '[CHAVE_API_REMOVIDA]', sanitized)
        
        return sanitized