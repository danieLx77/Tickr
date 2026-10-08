# Resultados e matriz de validação

**Atualizado em 08/10/2026.** “Local” significa nesta máquina; não comprova hospedagem ou plano gratuito remoto. Testes usaram somente registros sintéticos. Nenhuma execução agendada real, envio de e-mail ou upload externo foi observada.

| Componente | Estado | Evidência e limitação |
| --- | --- | --- |
| Frontend remoto HTTPS | **Pendente** | `npm run build` passou localmente; sem projeto Vercel/URL remota. |
| Backend FastAPI remoto | **Pendente** | TestClient e servidor Uvicorn local passaram; sem Vercel. |
| Comunicação frontend–backend remota | **Pendente** | Interface preparada para `VITE_API_URL`, sem teste remoto. |
| PostgreSQL persistente | **Aprovado com restrições** | Docker local: escrita/leitura e `synthetic|1` após reinício; Projeto Neon Free criado, mas conexão e persistência remotas não testadas. |
| Commit e rollback | **Aprovado com restrições** | Teste local confirmou escrita e ausência do marcador `rollback_probe`; não executado em Neon. |
| Escrita não autorizada bloqueada | **Aprovado com restrições** | API local respondeu 401 sem token em TestClient e HTTP real; autenticação simplificada, não final. |
| Agendamento automático real | **Pendente** | Workflow preparado; nenhum disparo `schedule` observado. Execução manual não o substituirá. |
| Job idempotente/recuperação | **Aprovado com restrições** | Local: duas janelas ausentes inseridas, reexecução retornou `inserted: False` para ambas; recuperação limitada a 24 horas. |
| E-mail real autorizado | **Pendente** | Sem conta Resend e sem destinatário autorizado. |
| Backup criptografado externo | **Pendente** | Dump local criptografado com AES-256-CBC/PBKDF2 e checksum validado; não enviado a destino externo. |
| Restauração isolada | **Aprovado com restrições** | Dump local restaurado em PostgreSQL 17 isolado; consulta deu `synthetic|1`. Não testado em ambiente remoto. |
| Segredos protegidos e HTTPS | **Pendente** | Código evita segredos no Git e protege escrita; HTTPS remoto e configuração de segredos não testados. |
| Custo R$ 0 integral | **Pendente** | Cotas oficiais pesquisadas, nenhuma conta/projeto remoto medido. |
| Operação sem computador pessoal | **Pendente** | Jobs, API e banco só testados localmente. |

## Verificações locais executadas

- Instalação das dependências Python e Node; `npm install` relatou 0 vulnerabilidades entre 22 pacotes auditados naquele momento.
- `ruff check backend` e `ruff format --check backend`: passaram.
- `pytest -q backend/tests` com PostgreSQL Docker local: **4 testes passaram** na execução final (1 aviso de depreciação do TestClient).
- `npm run build`: passou, Vite gerou `dist/`.
- Uvicorn local iniciou e respondeu HTTP 200 para `/health`, `/db` e `/records/demo`; `POST /records` sem token respondeu 401.
- `scripts/backup.sh`: gerou arquivo criptografado e checksum local.
- Primeira restauração no PostgreSQL 16 falhou porque o `pg_dump`/`pg_restore` do host são versão 17 e o dump contém `transaction_timeout` desconhecido no servidor 16. Restauração em PostgreSQL 17 isolado passou, inclusive com a versão final do script transacional. Isso demonstra necessidade de compatibilidade de versões no procedimento remoto.
- Reinício do PostgreSQL local preservou o registro e o job (`synthetic|1`).
- `backend/job.py --recover-hours 2` inseriu dois horários lógicos; reexecução das mesmas janelas não inseriu duplicatas.

## Falhas simuladas e não simuladas

`DATABASE_URL` ausente produziu 503 sem expor a variável. Acesso sem token produziu 401. Não foram simuladas indisponibilidade real do Neon, falha de e-mail, atraso do agendador, falha de upload externo nem saturação de cotas. O teste local de `TestClient` precisou rodar fora do sandbox por restrição do ambiente; isso não é evidência remota.

## Pendências de observação remota

Depois de configurar os serviços com autorização: registrar URL HTTPS e horários, executar leitura/escrita/reinício em Neon, rodar workflow manual e aguardar um `schedule` real, comparar horários planejado/efetivo, repetir job, verificar consumo, enviar mensagem sintética ao destinatário autorizado, baixar o artefato criptografado e restaurá-lo em banco remoto isolado. Registrar links de execuções e IDs não sensíveis. Não deixar uma sessão aberta indefinidamente aguardando cron.
