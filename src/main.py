from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.infrastructure.api.routes import router as security_router
from src.infrastructure.api.secret_routes import router as vault_router
from src.infrastructure.api.llm_routes import router as llm_router
from src.infrastructure.database.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Executa na inicialização da aplicação
    await init_db()
    yield

app = FastAPI(
    title="SentinelCore - AI & Secrets Gateway",
    description="API de Segurança e Proxy Intermediário para LLMs",
    version="1.0.0",
    lifespan=lifespan
)

# Registra as rotas da nossa aplicação
app.include_router(security_router)
app.include_router(vault_router)
app.include_router(llm_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "service": "SentinelCore IS ALIVE"}