from src.domain.crypto import EnvelopeCryptoManager
from src.domain.sanitizer import PromptSanitizer
from src.application.schemas import PromptRequest, PromptResponse
from src.infrastructure.config import settings

class SanitizePromptUseCase:
    """
    Orquestra a higienização simples de prompts recebidos pela API.
    """
    @staticmethod
    def execute(request: PromptRequest) -> PromptResponse:
        # Chama a nossa regra de domínio pura
        sanitized = PromptSanitizer.sanitize(request.prompt_text)
        # Retorna o modelo de resposta
        return PromptResponse(
            original_text=request.prompt_text,
            sanitized_text=sanitized
        )


class ExecuteSecureLLMUseCase:
    """
    Orquestra o fluxo completo: recupera a chave do Vault,
    sanitiza o prompt e simula a execução na LLM.
    """
    @staticmethod
    async def execute(secret_record, raw_prompt: str) -> dict:
        # Descriptografa a chave em memória apenas durante o processamento
        crypto = EnvelopeCryptoManager(master_secret=settings.MASTER_KEY)
        decrypted_api_key = crypto.decrypt(secret_record.encrypted_value)
        
        # Sanitiza o prompt original
        sanitized_prompt = PromptSanitizer.sanitize(raw_prompt)
        
        # Simula a chamada com a chave e o prompt limpo
        return {
            "status": "processed_securely",
            "vault_secret_used": secret_record.name,
            "sanitized_prompt": sanitized_prompt,
            "simulated_llm_response": f"Resposta gerada pela IA com sucesso para o prompt: '{sanitized_prompt}'"
        }