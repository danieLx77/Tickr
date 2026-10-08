# Fase 00 — PoC de infraestrutura gratuita

**Estado em 08/10/2026: pendente.** A interface, a API e o banco sintético funcionam remotamente por HTTPS; o job manual e o backup criptografado foram executados no GitHub Actions, um artefato baixado foi restaurado em PostgreSQL 18 isolado, e um e-mail sintético foi entregue. Ainda falta observar um disparo **real** de `schedule`, resolver o envio permanente sem domínio pago e comprovar a política completa de retenção e custo R$ 0 em uso continuado. A Fase 01 permanece bloqueada.

## Serviços implantados

| Serviço | Endereço / projeto | Evidência |
| --- | --- | --- |
| Interface React/TypeScript | [Tickr PoC](https://frontend-rust-one-50.vercel.app/) — Vercel Hobby | HTTPS, build de produção, leitura de `demo` e estados da API/banco no navegador; largura móvel de 390 px sem rolagem horizontal. |
| API FastAPI | [Health check](https://backend-lake-one-89.vercel.app/health) — Vercel Hobby | `/health`, `/db`, leitura e escrita autenticada, 401 sem token e rollback testados por HTTPS. |
| PostgreSQL | [Neon `tickr-poc`](https://console.neon.tech/app/projects/twilight-poetry-23702290) — Free, São Paulo | Duas tabelas e registros sintéticos; API e Actions acessaram via TLS. Leitura persistiu após novo deploy da API. |
| Job | [Execução inicial](https://github.com/danieLx77/Tickr/actions/runs/37803072113), [reexecução](https://github.com/danieLx77/Tickr/actions/runs/37803453232) | O primeiro gravou `inserted: True`; o segundo, `False`. Consulta Neon mostrou uma única linha para a chave lógica. Ambos foram manuais. |
| Backup | [Execução com artefato](https://github.com/danieLx77/Tickr/actions/runs/37803587635) | Dump criptografado e checksum armazenados no GitHub; download, SHA-256 e restauração isolada testados. Artefato expira em 90 dias. |
| E-mail | [Resend: mensagem de teste](https://resend.com/emails/01a11c38-33da-796a-81eb-adbcd4a8b44b) | `Sent` e `Delivered` para o endereço GitHub autorizado, usando `onboarding@resend.dev`. Esse domínio serve para teste; produção exige solução verificada. |

Dados são exclusivamente sintéticos. A autenticação por token demonstra bloqueio de escrita, mas não substitui Argon2id, TOTP, sessões revogáveis e regras de acesso da Fase 02. Os projetos Vercel estão na equipe Hobby `tickr4`; o repositório GitHub é público. Segredos estão nas variáveis Secret da Vercel e nos Secrets do GitHub Actions, fora do Git. A frase de recuperação do backup também está no arquivo local ignorado `.poc-secrets/backup-passphrase`; o proprietário deve guardar uma cópia segura independente do computador.

## Pendências essenciais

1. Observar pelo menos um evento `schedule` real do job às `HH:17` UTC e registrar horário efetivo e persistência no Neon. A execução manual não aprova o agendador. O GitHub pode atrasar ou perder eventos; o job recupera até três janelas recentes na execução agendada.
2. Demonstrar envio contínuo permitido em produção sem compra de domínio. O Resend entregou um teste ao próprio usuário, mas recomenda domínio verificado para produção; avaliar alternativa gratuita compatível.
3. Validar a retenção 7 diários/4 semanais/3 mensais e o consumo de armazenamento. Artefatos Actions são independentes do Neon, mas expiram em 90 dias e somem com a exclusão do repositório/workflow.
4. Medir cotas após operação representativa; a ausência de cobrança nos testes de hoje não garante R$ 0 de forma permanente.

Ver [provedores](providers-evaluation.md), [consumo](cost-estimate.md), [resultados](test-results.md) e [recuperação](recovery-procedures.md). Não iniciar a Fase 01 enquanto a matriz mantiver requisitos essenciais pendentes.
