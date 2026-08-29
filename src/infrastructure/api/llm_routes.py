from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from pydantic import BaseModel, Field

from src.infrastructure.database.session import get_session
from src.infrastructure.database.models import SecretModel
from src.infrastructure.security.rate_limiter import RateLimiter
from src.application.use_cases import ExecuteSecureLLMUseCase
from src.domain.audit import SecurityAuditEvent
from src.infrastructure.logging.audit_logger import AuditLogger

router = APIRouter(prefix="/api/v1/llm", tags=["LLM Gateway Proxy"])

class LLMExecutionRequest(BaseModel):
    secret_name: str = Field(..., example="OPENAI_API_KEY", description="Nome do segredo cadastrado no Vault")
    prompt: str = Field(..., example="Resuma o contrato do cliente joao@empresa.com de CPF 111.222.333-44", description="Prompt com dados sensíveis")

@router.post("/generate")
async def generate_llm_response(
    payload: LLMExecutionRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_session)
):
    """
    Endpoint Proxy Central:
    - Aplica Rate Limiting por IP no Redis (Max 5 req/min)
    - Busca e descriptografa a chave do Vault (Postgres)
    - Mascara dados sensíveis do prompt (Sanitizer)
    - Executa a chamada segura
    """
    # Controle de Taxa (Redis)
    client_ip = request.client.host or "127.0.0.1"
    await RateLimiter.check_rate_limit(client_id=client_ip, limit=5, window_seconds=60)
    
    # Busca no Vault
    query = select(SecretModel).where(SecretModel.name == payload.secret_name)
    result = await db.execute(query)
    secret_record = result.scalars().first()
    
    if not secret_record:
        # Dispara auditoria de tentativa de acesso não autorizado/inválido
        audit_event = SecurityAuditEvent.create(
            event_type="VAULT_ACCESS_FAILED",
            client_ip=client_ip,
            secret_used=payload.secret_name,
            status="FAILURE",
            details="Tentativa de acesso a um segredo inexistente no Vault."
        )
        background_tasks.add_task(AuditLogger.log_event, audit_event)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"O segredo '{payload.secret_name}' não foi encontrado no Vault."
        )

    # Processamento do Caso de Uso
    response = await ExecuteSecureLLMUseCase.execute(secret_record, payload.prompt)
    
    # Dispara Auditoria em Segundo Plano (Zero overhead na resposta)
    audit_event = SecurityAuditEvent.create(
        event_type="PROMPT_SANITIZED_AND_EXECUTED",
        client_ip=client_ip,
        secret_used=secret_record.name,
        status="SUCCESS",
        details="Prompt higienizado e enviado com sucesso ao provedor de IA."
    )
    background_tasks.add_task(AuditLogger.log_event, audit_event)

    return response