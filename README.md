# Tickr

Tickr é uma aplicação web pessoal para acompanhar uma carteira de ações da B3, proventos e oportunidades segundo os critérios de Décio Bazin. Serve a um único administrador, em português brasileiro. BESST (Bancos, Energia, Saneamento, Seguros e Telecomunicações) organiza análises; ações de outros setores também são acompanhadas. Indicadores, cores e ranking não constituem recomendação de investimento.

**Estado:** Fase 00 em execução, com protótipo e testes locais. A infraestrutura remota e o custo R$ 0 ainda não foram validados; a PoC está pendente e antecede a implementação funcional.

## Escopo e arquitetura planejados

O MVP inclui operações manuais e retroativas, uma carteira, posições e resultados, proventos esperados e recebidos, DPA e DY, preço-teto, Watchlist e Oportunidades separadas, alertas e resumo semanal por e-mail, gráficos históricos confiáveis, TWR e comparação com Ibovespa/IDIV quando houver dados, exportação CSV/JSON, auditoria, monitoramento e backup com restauração. A interface será responsiva, com sete áreas e temas claro/escuro. Não haverá ordens, corretoras, cadastro público, importação CSV, restauração JSON pela interface, aplicativo nativo ou PWA instalável no MVP.

A stack escolhida para a aplicação é React/TypeScript, Python/FastAPI, PostgreSQL, API REST e monólito modular em monorepo. Docker Compose é planejado para desenvolvimento local. Vercel, Neon, GitHub Actions e Resend são **candidatos**, sujeitos à PoC; fontes de dados e limites gratuitos também precisam de validação. A operação deve custar **R$ 0**, funcionar na nuvem com o computador pessoal desligado e não depender de domínio ou serviço pago.

## Desenvolvimento local

A PoC local usa Python 3.12+, Node.js 22, npm e Docker Compose. Com PostgreSQL iniciado por `docker compose up -d`, instale dependências em um ambiente virtual com `pip install -r backend/requirements-dev.txt`; execute `pytest -q backend/tests` com `POC_TEST_DATABASE_URL` apontando ao banco sintético local. Para a interface, use `npm ci` e `npm run build` em `frontend/`. Configure `DATABASE_URL`, `POC_DB_SSLMODE=disable` apenas no banco local, `POC_WRITE_TOKEN` e `POC_CORS_ORIGINS` fora do Git. Os exemplos ficam em `backend/.env.example` e `frontend/.env.example`. A implantação remota permanece pendente; veja [resultados da PoC](docs/poc/README.md).

## Documentação

- [Requisitos e aceite](docs/requirements.md)
- [Arquitetura e segurança](docs/architecture.md)
- [Modelo de dados](docs/data-model.md)
- [Regras financeiras](docs/financial-rules.md)
- [Fontes externas](docs/data-sources.md)
- [Estratégia de testes](docs/test-strategy.md)
- [Plano de implementação e pendências](docs/implementation-plan.md)
- [Operações e recuperação](docs/operations.md)
- [Decisões arquiteturais](docs/adr/README.md)
- [Instruções para agentes](AGENTS.md)
- [Resultados da Fase 00](docs/poc/README.md)

Provedores, termos de acesso, cobertura histórica, tributação e operação gratuita ainda dependem das validações registradas nos documentos.
