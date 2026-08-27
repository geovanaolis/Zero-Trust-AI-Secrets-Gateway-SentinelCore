from fastapi import APIRouter
from src.application.schemas import PromptRequest, PromptResponse
from src.application.use_cases import SanitizePromptUseCase

# Cria um roteador para organizar nossos endpoints
router = APIRouter(prefix="/api/v1/security", tags=["Security Gateway"])

@router.post("/sanitize", response_model=PromptResponse)
async def sanitize_prompt(request: PromptRequest):
    """
    Endpoint de segurança para higienizar prompts antes do envio para LLMs.
    """
    # Toda a lógica complexa está encapsulada no Caso de Uso!
    return SanitizePromptUseCase.execute(request)