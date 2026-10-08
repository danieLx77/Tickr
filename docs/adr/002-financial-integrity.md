# ADR-002 — Fonte de verdade financeira e precisão

**Estado:** aceita.

## Contexto

Operações retroativas, correções de fontes, eventos societários e rendimentos tornam caches e números binários inadequados como fonte de verdade.

## Decisão e justificativa

Preservar eventos financeiros originais/versionados e auditoria; usar `Decimal`/`NUMERIC`, identidade estável de instrumento e transações atômicas. Reconstruir cronologicamente derivados após correções; rejeitar histórico inconsistente, manter recebimento confirmado e invalidar caches por versão. Isso permite reproduzir cálculos e explicar divergências.

## Consequências e alternativas

Exige controle de concorrência, idempotência, testes financeiros e tratamento de reconstrução longa. Ticker como chave, `float`, sobrescrita de origem e caches como verdade foram rejeitados. TWR/caixa técnico, bonificação e arredondamento específico permanecem pendentes em [P-12/P-13/P-16](../implementation-plan.md).
