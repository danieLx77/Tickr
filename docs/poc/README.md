# Fase 00 — PoC de infraestrutura gratuita

**Estado em 08/10/2026: pendente.** Há protótipo mínimo React/TypeScript, API FastAPI, PostgreSQL local sintético, job idempotente e mecanismo local de backup criptografado/restauração. Contas gratuitas Vercel Hobby e Neon Free foram acessadas; o projeto Neon `tickr-poc` foi criado em São Paulo. Não houve implantação remota, conexão com Neon, conta Resend, envio real de e-mail, execução agendada observada nem backup armazenado externamente. Portanto, a exigência de operação integralmente remota por R$ 0 **não foi comprovada**.

## Arquitetura efetivamente testada

Frontend gerado localmente com Vite; backend FastAPI testado localmente; PostgreSQL 16 local via Docker Compose para API/job e PostgreSQL 17 isolado para restauração do dump gerado por `pg_dump` 17. Dados são exclusivamente sintéticos. A API tem health check, conexão com banco, leitura, escrita com token temporário e transação com rollback. O job grava horários lógicos idempotentes e recupera até 24 janelas recentes. A autenticação da PoC é apenas demonstração de bloqueio de escrita; Argon2id, TOTP e sessões revogáveis são da Fase 02.

## Caminho remoto proposto, ainda sem autorização/credenciais

Dois projetos Vercel a partir do monorepo, com raízes `frontend/` e `backend/`; variáveis `VITE_API_URL`, `DATABASE_URL`, `POC_WRITE_TOKEN` e `POC_CORS_ORIGINS` configuradas diretamente nos serviços. Neon como PostgreSQL; GitHub Actions para CI, job e backup criptografado; Resend em avaliação. Nenhum desses componentes remotos foi testado ou aprovado. Segredos nunca devem ser enviados pelo chat nem inseridos em arquivos versionados. Publicar serviços exige autorização apropriada.

## Bloqueios e próximos passos

As contas Vercel/Neon e a reconexão do GitHub CLI foram autorizadas e criadas/concluídas. Para completar a PoC: conectar o banco Neon ao backend sem expor segredos, publicar frontend/API gratuitos, configurar variáveis nos painéis, executar testes HTTPS, observar cron real, receber um endereço de e-mail autorizado e testar envio, guardar backup criptografado em destino externo e restaurá-lo em banco remoto isolado. Confirmar ausência de cobrança automática e termos antes de cada serviço. Ver [provedores](providers-evaluation.md), [consumo](cost-estimate.md), [resultados](test-results.md) e [recuperação](recovery-procedures.md). A Fase 01 permanece bloqueada.
