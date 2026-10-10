# Resultados e matriz de validação

**Atualizado em 10/10/2026.** Somente dados sintéticos foram usados. “Aprovado” refere-se ao teste indicado, não à aprovação geral da PoC.

| Componente | Estado | Evidência e limitação |
| --- | --- | --- |
| Frontend remoto HTTPS | **Aprovado** | [Página pública](https://frontend-rust-one-50.vercel.app/) abriu; build Vite passou. Em 390 px não houve rolagem horizontal. |
| Backend FastAPI remoto | **Aprovado** | [Health check](https://backend-lake-one-89.vercel.app/health) retornou 200 e fase 00. |
| Comunicação frontend–backend | **Aprovado** | Navegador exibiu API/banco conectados e leu `demo` do Neon; preflight CORS da origem exata retornou 200. |
| PostgreSQL persistente | **Aprovado com restrições** | Neon Free: escrita HTTPS 201, leitura 200 e dados presentes depois de novo deploy da API. Teste de suspensão prolongada/limite de CU-h ainda pendente. |
| Commit e rollback | **Aprovado** | Escrita `demo` persistiu; `/transaction-check` remoto retornou `rollback_ok: true`. |
| Escrita não autorizada bloqueada | **Aprovado com restrições** | POST sem token retornou 401. Token temporário da PoC não é autenticação final. |
| Agendamento automático real | **Aprovado com restrições** | O histórico contém oito runs `event=schedule` concluídos com sucesso entre 08 e 10/10; [exemplo de 10/10](https://github.com/danieLx77/Tickr/actions/runs/38063552250) com etapa do job aprovada. Isto comprova o disparo real, não a cadência horária. |
| Cadência horária e recuperação | **Reprovado** | Na amostra houve intervalos de aproximadamente 4–7 horas entre runs reais; `--recover-hours 3` cobre menos que essas lacunas. Não há evidência de recuperação integral dos horários perdidos. |
| Job idempotente/recuperação | **Aprovado com restrições** | [Primeiro run](https://github.com/danieLx77/Tickr/actions/runs/37803072113): `inserted: True`, planejado 15:00 UTC, efetivo 15:43:31 UTC por disparo manual. [Reexecução](https://github.com/danieLx77/Tickr/actions/runs/37803453232): `False`; Neon mostrou contagem 1. Recuperação de duas janelas passou localmente, ainda não em um `schedule` real. |
| E-mail real autorizado | **Aprovado com restrições** | [Resend](https://resend.com/emails/01a11c38-33da-796a-81eb-adbcd4a8b44b) registrou `Sent` e `Delivered` para o endereço GitHub autorizado. Chave com `Sending access` em GitHub Secret. `resend.dev` é domínio de teste; uso contínuo em produção sem domínio próprio permanece pendente. |
| Backup criptografado externo | **Aprovado com restrições** | [Actions 37803587635](https://github.com/danieLx77/Tickr/actions/runs/37803587635) publicou `.dump.enc` e `.sha256`; download e SHA-256 passaram. Dois backups `schedule` também passaram: [09/10](https://github.com/danieLx77/Tickr/actions/runs/37920217758) e [10/10](https://github.com/danieLx77/Tickr/actions/runs/38043708590). O workflow não implementa seleção/rotação 7/4/3. |
| Restauração isolada | **Aprovado** | Artefato baixado foi descriptografado e restaurado em PostgreSQL 18 local isolado. `demo`, `synthetic`, job e restrições de chave/check foram verificados. Nenhuma restauração sobre Neon principal. |
| Segredos protegidos e HTTPS | **Aprovado com restrições** | HTTPS nas duas URLs; Vercel Secret para `DATABASE_URL`/token, GitHub Secrets para conexão/chave. Repositório público contém só código e dados sintéticos; a chave de backup precisa de cópia segura pelo proprietário. |
| Custo R$ 0 integral | **Pendente** | Contas Hobby/Free sem contratação paga nos testes; medição continuada e viabilidade do e-mail/retenção incompletas. |
| Operação sem computador pessoal | **Aprovado com restrições** | Frontend, API, PostgreSQL, job e backup executam na nuvem. Cron e e-mail permanecem sem prova completa. |

## Execuções e falhas observadas

- CI [37803575716](https://github.com/danieLx77/Tickr/actions/runs/37803575716) passou. Localmente: Ruff, build Vite, quatro testes Python com PostgreSQL Docker, health/leitura/escrita/rollback HTTP e recuperação de duas janelas passaram.
- O primeiro [backup remoto](https://github.com/danieLx77/Tickr/actions/runs/37803119638) falhou porque o Neon usa PostgreSQL 18 e o runner tinha `pg_dump` 16. O workflow agora usa a imagem oficial `postgres:18`; [run corrigido](https://github.com/danieLx77/Tickr/actions/runs/37803587635) passou.
- A primeira tentativa de repetir o job [falhou](https://github.com/danieLx77/Tickr/actions/runs/37803163650) com `UndefinedTable: poc_job_runs`. A mesma configuração, a consulta ao Neon e a repetição manual não reproduziram a falha; os oito runs agendados posteriores passaram. Causa não identificada nos logs/configuração disponíveis, sem correção especulativa.
- O checksum inicial continha caminho absoluto do container, o que impedia sua verificação após download. O script foi corrigido para nome relativo; o artefato novo passou SHA-256 fora do runner.
- Sem `DATABASE_URL`, a API local respondeu 503 sem vazar credenciais; sem token, 401. Não foram simuladas indisponibilidade prolongada do Neon, falha de envio, atraso real do agendador ou saturação de cotas.

## Como verificar o cron depois

No [histórico do job](https://github.com/danieLx77/Tickr/actions/workflows/poc-job.yml), distinguir `schedule` de `workflow_dispatch`; os runs reais já provam o disparo. Para avaliar a recuperação, comparar as chaves `poc-hourly-AAAAMMDDHH` persistidas com todas as horas esperadas, inclusive as lacunas entre runs. O cron está em `17 * * * *` UTC, mas a amostra não sustentou frequência horária. Aumentar a janela de recuperação além das lacunas observadas é a correção mínima proposta, sujeita a teste direcionado futuro.
