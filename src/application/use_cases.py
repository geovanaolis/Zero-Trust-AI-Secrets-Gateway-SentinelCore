from src.domain.sanitizer import PromptSanitizer
from src.application.schemas import PromptRequest, PromptResponse

class SanitizePromptUseCase:
    """
    Orquestra o fluxo: Recebe o request validado, passa pelo motor de 
    sanitização (Core) e constrói a resposta formatada.
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