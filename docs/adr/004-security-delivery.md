# ADR-004 — Segurança, jobs e fluxo de entrega

**Estado:** aceita; detalhes de provisionamento e garantias de e-mail dependem de validação.

## Contexto

Dados financeiros pessoais, administrador único, jobs possivelmente externos à API serverless e fluxo de desenvolvimento sem PR obrigatório pedem controles explícitos.

## Decisão e justificativa

Login com Argon2id e TOTP obrigatório, recuperação de uso único, sessões revogáveis por até sete dias, cookies seguros, HTTPS, CSRF, rate limiting e autorização. Jobs independentes da execução serverless da API, com estado persistido e idempotência. Desenvolvimento diretamente na `main`, Conventional Commits em inglês, verificações locais e CI em push relevante; deploy somente com CI aprovada.

## Consequências e alternativas

Provisionamento inicial e envio confiável exigem PoC/testes. A CI detecta problemas após push e protege principalmente o deploy; sem PR, revisão local e testes ganham peso. Cron dentro da API serverless e e-mail sem estado durável são inadequados. Aprovação automática de verificações não substitui aceite funcional manual. Ver [segurança](../architecture.md) e [testes](../test-strategy.md).
