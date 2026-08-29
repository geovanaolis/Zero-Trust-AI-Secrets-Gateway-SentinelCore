from datetime import datetime, timezone
from pydantic import BaseModel

class SecurityAuditEvent(BaseModel):
    """
    Modelo de evento de auditoria alinhado com padrões SIEM (Datadog, Splunk, Elastic).
    """
    timestamp: str
    event_type: str  # Ex: "PROMPT_SANITIZED", "VAULT_ACCESS", "RATE_LIMIT_EXCEEDED"
    client_ip: str
    secret_used: str
    status: str
    details: str

    @classmethod
    def create(cls, event_type: str, client_ip: str, secret_used: str, status: str, details: str):
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            client_ip=client_ip,
            secret_used=secret_used,
            status=status,
            details=details
        )