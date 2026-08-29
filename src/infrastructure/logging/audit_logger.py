import json
import logging
from src.domain.audit import SecurityAuditEvent

# Configura o logger padrão para saída estruturada
logger = logging.getLogger("sentinelcore.audit")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

class AuditLogger:
    """
    Serviço assíncrono para publicação de logs de auditoria imutáveis.
    """
    @staticmethod
    def log_event(event: SecurityAuditEvent):
        # Em produção corporativa, este método envia o evento para o Apache Kafka
        log_json = json.dumps(event.model_dump())
        logger.info(f"[AUDIT_EVENT] {log_json}")