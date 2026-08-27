from fastapi import FastAPI
from src.infrastructure.api.routes import router as security_router

app = FastAPI(
    title="SentinelCore - AI & Secrets Gateway",
    description="API de Segurança e Proxy Intermediário para LLMs",
    version="1.0.0"
)

# Registra as rotas da nossa aplicação
app.include_router(security_router)

@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint para monitoramento de infraestrutura (Kubernetes/Docker)."""
    return {"status": "ok", "service": "SentinelCore IS ALIVE"}