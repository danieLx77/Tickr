# Fase 00 — PoC de infraestrutura gratuita

**Estado em 10/10/2026: pendente.** A interface, a API e o banco sintético funcionam remotamente por HTTPS; o job e o backup criptografado tiveram disparos agendados reais, um artefato foi restaurado em PostgreSQL 18 isolado, e um e-mail sintético foi entregue. A recuperação por lacunas passou localmente, mas ainda requer validação remota; seguem sem validação o envio permanente sem domínio pago, a retenção 7/4/3 e o custo R$ 0 integral. A Fase 01 permanece bloqueada.

## Serviços implantados

| Serviço | Endereço / projeto | Evidência |
| --- | --- | --- |
| Interface React/TypeScript | [Tickr PoC](https://frontend-rust-one-50.vercel.app/) — Vercel Hobby | HTTPS, build de produção, leitura de `demo` e estados da API/banco no navegador; largura móvel de 390 px sem rolagem horizontal. |
| API FastAPI | [Health check](https://backend-lake-one-89.vercel.app/health) — Vercel Hobby | `/health`, `/db`, leitura e escrita autenticada, 401 sem token e rollback testados por HTTPS. |
| PostgreSQL | [Neon `tickr-poc`](https://console.neon.tech/app/projects/twilight-poetry-23702290) — Free, São Paulo | Duas tabelas e registros sintéticos; API e Actions acessaram via TLS. Leitura persistiu após novo deploy da API. |
| Job | [Execução agendada](https://github.com/danieLx77/Tickr/actions/runs/38063552250), [reexecução manual](https://github.com/danieLx77/Tickr/actions/runs/37803453232) | Oito eventos `schedule` passaram; a reexecução manual foi idempotente. Os intervalos de 4–7 horas motivaram a correção local da recuperação; falta validação remota desta versão. |
| Backup | [Execução com artefato](https://github.com/danieLx77/Tickr/actions/runs/37803587635), [agendamento de 10/10](https://github.com/danieLx77/Tickr/actions/runs/38043708590) | Dump criptografado, checksum e restauração isolada testados; dois backups agendados passaram. O artefato expira em 90 dias. |
| E-mail | [Resend: mensagem de teste](https://resend.com/emails/01a11c38-33da-796a-81eb-adbcd4a8b44b) | `Sent` e `Delivered` para o endereço GitHub autorizado, usando `onboarding@resend.dev`. Esse domínio serve para teste; produção exige solução verificada. |

Dados são exclusivamente sintéticos. A autenticação por token demonstra bloqueio de escrita, mas não substitui Argon2id, TOTP, sessões revogáveis e regras de acesso da Fase 02. Os projetos Vercel estão na equipe Hobby `tickr4`; o repositório GitHub é público. Segredos estão nas variáveis Secret da Vercel e nos Secrets do GitHub Actions, fora do Git. A frase de recuperação do backup também está no arquivo local ignorado `.poc-secrets/backup-passphrase`; o proprietário deve guardar uma cópia segura independente do computador.

## Pendências essenciais

1. Validar remotamente a recuperação por lacunas persistidas após um disparo real. Os testes locais passaram; o GitHub ainda pode atrasar ou perder eventos, e a execução processa no máximo 24 pendências por vez.
2. Demonstrar envio contínuo permitido em produção sem compra de domínio. O Resend entregou um teste ao próprio usuário, mas recomenda domínio verificado para produção; avaliar alternativa gratuita compatível.
3. Definir e validar a retenção 7 diários/4 semanais/3 mensais e o consumo de armazenamento. O workflow atual guarda todos os dumps por 90 dias, sem seleção 7/4/3; artefatos somem com a exclusão do repositório/workflow.
4. Medir cotas após operação representativa; a ausência de cobrança nos testes de hoje não garante R$ 0 de forma permanente.

Ver [provedores](providers-evaluation.md), [consumo](cost-estimate.md), [resultados](test-results.md) e [recuperação](recovery-procedures.md). Não iniciar a Fase 01 enquanto a matriz mantiver requisitos essenciais pendentes.
