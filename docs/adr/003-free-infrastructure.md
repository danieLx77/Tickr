# ADR-003 — Custo zero e PoC anterior ao MVP

**Estado:** aceita para a restrição e a ordem; **dependente de validação** para provedores.

## Contexto

O Tickr deve operar por R$ 0, na nuvem, com computador pessoal desligado, incluindo jobs, e-mail e recuperação de dados. Planos gratuitos e termos podem mudar.

## Decisão e justificativa

Executar Fase 00 antes de implementação funcional: provar frontend/API remotos, PostgreSQL, agendamento, e-mail sem domínio pago, backup externo criptografado, restauração e segurança. Vercel, Neon, GitHub Actions e Resend são candidatos apenas. Adaptadores e desenho operacional devem permitir alternativa gratuita.

## Consequências e alternativas

Sem evidência de operação gratuita completa, a implementação funcional/implantação fica bloqueada. Não aceitar fallback pago nem presumir cron pontual, cota estável ou e-mail viável. Hospedagem doméstica permanente e serviço pago violam requisito. Ver [plano](../implementation-plan.md).
