# SentinelCore: Zero-Trust AI & Secrets Gateway

O **SentinelCore** é uma API back-end atuando como proxy de segurança e cofre centralizado para aplicações corporativas. Desenvolvido sob os princípios da Arquitetura Hexagonal, ele previne vazamento de dados (*Data Leakage*) para LLMs e gerencia credenciais criptografadas com rastreabilidade total.

## Arquitetura e Fluxo de Dados
O sistema atua como um "pedágio inteligente" entre as aplicações internas e os provedores externos de Inteligência Artificial.
1. O cliente envia um prompt e a indicação de uma chave via API REST.
2. O **Rate Limiter (Redis)** intercepta o tráfego para validar cotas por IP (Anti-DoS).
3. O **Core de Segurança** varre e sanitiza o texto mascarando informações sensíveis (PII).
4. O sistema consulta o **Vault (PostgreSQL)** para descriptografar a API Key original temporariamente.
5. A chamada segura é simulada e um **Log de Auditoria** assíncrono é disparado em background.

## Principais Funcionalidades
* **Motor de Sanitização (Guardrail):** Regras de domínio em Python puro que detectam e ocultam CPFs, E-mails e chaves expostas no prompt em tempo real.
* **Cofre de Segredos (Vault):** Aplicação de *Envelope Encryption* (AES-256), garantindo que as chaves de acesso externas sejam salvas em repouso de forma ininteligível.
* **Proteção de Camada de Rede:** Bloqueio de abusos de cota (ex: limite de 5 req/minuto) implementado com Redis para preservar o orçamento (Billing) da empresa.
* **Trilha de Auditoria (Security Logs):** Emissão de registros imutáveis em JSON via `BackgroundTasks`, prontos para ingestão em ferramentas SIEM corporativas sem onerar a latência.

## Tecnologias Utilizadas
* **FastAPI & Pydantic:** Framework assíncrono validando estritamente os contratos de entrada e saída.
* **PostgreSQL (SQLModel):** Persistência relacional isolada para o cofre.
* **Redis:** Cache distribuído em memória para controle temporal.
* **Docker & DevSecOps:** Infraestrutura orquestrada via `docker-compose` e esteira de CI/CD garantindo análise estática de segurança constante (SAST com Bandit).

## Como Executar e Testar
* Clone o repositório, instale as dependências e inicie o ambiente virtual (`venv`).
* Suba a infraestrutura de dados isolada executando `docker compose up -d`.
* Inicie o proxy rodando `uvicorn src.main:app --reload` e acesse o Swagger em `http://127.0.0.1:8000/docs` para interagir com o Vault e o Proxy IA.