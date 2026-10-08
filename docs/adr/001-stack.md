# ADR-001 — Monólito modular e stack

**Estado:** aceita.

## Contexto

Aplicação pessoal, um usuário, regras financeiras complexas e custo operacional obrigatório de R$ 0 exigem simplicidade e isolamento das integrações.

## Decisão e justificativa

Monorepo com frontend React/TypeScript, backend Python/FastAPI, API REST, PostgreSQL e Docker Compose local. Backend como monólito modular, separando domínio, aplicação, apresentação e infraestrutura. PostgreSQL oferece transações/restrições e `NUMERIC`; FastAPI/Python permitem regras decimais explícitas; adaptadores substituem fontes sem reescrever o domínio.

## Consequências e alternativas

Os módulos compartilham implantação e banco, exigindo fronteiras claras e testes de integração. Microsserviços adicionariam operação e custo sem necessidade atual. Hospedagem concreta não é definida neste ADR: depende da [PoC](003-free-infrastructure.md).
