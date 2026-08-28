from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.infrastructure.database.session import get_session
from src.infrastructure.database.models import SecretModel
from src.application.schemas import SecretCreateRequest, SecretResponse
from src.domain.crypto import EnvelopeCryptoManager
from src.infrastructure.config import settings

router = APIRouter(prefix="/api/v1/vault", tags=["Vault & Secrets"])
crypto = EnvelopeCryptoManager(master_secret=settings.MASTER_KEY)

@router.post("/secrets", response_model=SecretResponse, status_code=status.HTTP_201_CREATED)
async def store_secret(
    payload: SecretCreateRequest, 
    db: AsyncSession = Depends(get_session)
):
    """Criptografa a chave sensível e salva no banco de dados."""
    # Criptografa o valor em memória antes do banco
    encrypted = crypto.encrypt(payload.value)

    # Cria o registro
    secret_record = SecretModel(name=payload.name, encrypted_value=encrypted)
    
    try:
        db.add(secret_record)
        await db.commit()
        await db.refresh(secret_record)
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Secret com este nome já existe.")

    return SecretResponse(name=secret_record.name)