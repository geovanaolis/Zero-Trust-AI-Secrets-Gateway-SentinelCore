from pydantic import BaseModel, Field

class PromptRequest(BaseModel):
    # Field garante que o prompt seja uma string e tenha um tamanho máximo,
    # prevenindo ataques de negação de serviço (DoS) por payloads gigantes.
    prompt_text: str = Field(..., max_length=5000, description="O texto original do prompt")

class PromptResponse(BaseModel):
    original_text: str
    sanitized_text: str
    status: str = "success"