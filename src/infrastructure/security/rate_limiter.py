import redis.asyncio as redis
from fastapi import HTTPException, status

# Conexão assíncrona com o Redis rodando no Docker (porta 6379)
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

class RateLimiter:
    """
    Serviço de segurança para prevenção de DoS e controle de custos de API.
    Utiliza o Redis para rastrear requisições por IP do cliente.
    """
    @staticmethod
    async def check_rate_limit(client_id: str, limit: int = 5, window_seconds: int = 60):
        key = f"rate_limit:{client_id}"
        current_requests = await redis_client.get(key)
        
        if current_requests and int(current_requests) >= limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Limite de requisições excedido (Max 5 por minuto). Proteção ativa contra DoS."
            )
        
        async with redis_client.pipeline() as pipe:
            pipe.incr(key)
            if not current_requests:
                pipe.expire(key, window_seconds)
            await pipe.execute()