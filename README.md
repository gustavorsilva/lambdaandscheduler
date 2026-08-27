# lambdaandscheduler

📘 Boas Práticas de Observabilidade – Arquitetura IAM BFF
1. Objetivo

Garantir visibilidade ponta a ponta da arquitetura de autenticação e login, permitindo:

Detecção precoce de falhas.

Identificação de gargalos (API Gateway, Rate Limit, Redis, EKS).

Auditoria de acessos e segurança.

Métricas de performance e disponibilidade.

2. Pilares da Observabilidade
🔹 2.1 Logs

API Gateway

Ativar Access Logs e Execution Logs com requestId e integração ao DataDog.

Logar latência, status code, IP de origem e uso do Authorizer.

Lambda Authorizer

Capturar tentativas de autenticação falha (ex.: token inválido).

Logs estruturados em JSON (correlação por requestId).

NLB

Habilitar Access Logs no S3 e integrar com DataDog.

EKS (Pods: consumer-bff-login e BFF IAM)

Padrão structured logging (JSON).

Incluir campos de tracing (trace_id, span_id, sessionId).

Logs de erros críticos devem ser categorizados por severidade (INFO, WARN, ERROR, CRITICAL).

Quick Publisher

Logar eventos de publicação (sucesso, falha, latência).

Redis (Elasticache)

Habilitar logs de conexão/reconexão e falhas de operação.

Secret Manager

Monitorar logs de acesso a segredos via CloudTrail.

✅ Boa prática: centralizar logs no DataDog Log Management, aplicando pipelines para enriquecer com metadados (namespace, app, env).

🔹 2.2 Métricas

API Gateway

4XXError, 5XXError, Latency, IntegrationLatency, Requests.

Lambda Authorizer

Invocations, Duration, Errors, Throttles.

NLB

ProcessedBytes, ActiveFlowCount, TCP_Reset_Count.

EKS

CPU, Memory, Pod Restarts, Request Duration por rota.

Rate Limit Hits e Throttled Requests.

Redis (Elasticache)

CacheHits, CacheMisses, CurrConnections, Evictions, ReplicationLag.

Secret Manager

SecretsManagerAPIRequests, ThrottlingExceptions.

DataDog

Criar dashboards por domínio: Login Flow, Cache Health, Infra EKS, API Gateway.

✅ Boa prática: definir SLOs (ex.: 99.9% sucesso login, latência < 300ms).

🔹 2.3 Tracing Distribuído

Habilitar AWS X-Ray no API Gateway + Lambda + EKS.

Usar OpenTelemetry nos pods (consumer-bff-login, BFF IAM).

Propagar trace_id e sessionId em todos os headers HTTP.

Mapear:

Entrada (API Gateway → Lambda).

Chamada interna (NLB → consumer-bff-login → BFF IAM).

Dependências externas (Redis, Secret Manager).

✅ Boa prática: exportar traces para DataDog APM.

🔹 2.4 Alertas

API Gateway

Alerta para taxa de 5XXError > 1%.

Lambda Authorizer

Falhas de autenticação acima de baseline (anomalias).

Rate Limit

Requests bloqueadas > X% em Y minutos.

EKS

Restart frequente de pods (>3 em 10 min).

Latência do login > 500ms (p95).

Redis

Taxa de CacheMisses acima do baseline.

Latência de conexão > 50ms.

Secret Manager

Acessos suspeitos detectados via CloudTrail.

Infra geral

Falha no Quick Publisher deve gerar alerta imediato.

✅ Boa prática: usar alertas proativos (DataDog Monitor) com Auto-Remediation (ex.: restart pod via K8s operator).

3. Segurança e Compliance

Integrar CloudTrail para auditoria de IAM e Secret Manager.

Garantir que logs de autenticação sejam imutáveis (retidos em S3 + Lake Formation).

Monitorar anomalous login patterns (ex.: mesma conta usada de países diferentes).

4. Dashboards Recomendados

Login Performance

Latência (p50/p95/p99).

Sucesso x Erro de autenticação.

Infra EKS

CPU/Memória por pod.

Restarts por namespace.

API Gateway Health

Requests, Latência, 4XX/5XX.

Cache Eficácia

CacheHit Ratio.

Evictions.

Security Audit

Tentativas inválidas de login.

Acessos ao Secret Manager.

5. Checklist de Boas Práticas

 Logs estruturados e centralizados no DataDog.

 Tracing distribuído com X-Ray + OpenTelemetry.

 Dashboards organizados por domínio (Login, Infra, Cache, Security).

 SLOs definidos e monitorados.

 Alertas proativos configurados.

 Retenção de logs segura para auditoria.


 <img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/4feaf459-1e15-4fc4-b65c-aeff327b142b" />

