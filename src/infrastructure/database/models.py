from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class SecretModel(SQLModel, table=True):
    """
    Tabela que armazena APENAS dados cifrados no PostgreSQL.
    Nenhuma chave secreta em texto puro toca a persistência.
    """
    __tablename__ = "secrets"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, description="Nome identificador da chave (ex: OPENAI_KEY)")
    encrypted_value: str = Field(description="Valor da API Key criptografado com AES-256")
    created_at: datetime = Field(default_factory=datetime.utcnow)