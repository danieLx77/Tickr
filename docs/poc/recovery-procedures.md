# Procedimentos de backup e recuperação da PoC

Estes comandos são para **dados sintéticos** e ambiente controlado. O GitHub Actions armazenou um artefato criptografado externo ao Neon, ainda com restrições de retenção/capacidade. Nunca salvar `DATABASE_URL`, `BACKUP_PASSPHRASE` ou dumps em Git/logs. Fornecer segredos por gerenciador de ambiente/serviço, não pelo chat. A chave deve ficar separada do artefato. A cópia local ignorada `.poc-secrets/backup-passphrase` deve ser copiada pelo proprietário para um cofre seguro independente do computador. Não usar o banco principal como destino de restauração.

## Backup e integridade

Com cliente `pg_dump` compatível com o servidor de origem e destino, definir `DATABASE_URL`, `BACKUP_PASSPHRASE` e `BACKUP_OUTPUT_DIR` no ambiente e executar `bash scripts/backup.sh`. O script cria dump customizado consistente, criptografa com OpenSSL AES-256-CBC/PBKDF2 (250.000 iterações), grava SHA-256 do arquivo criptografado e verifica o checksum. O arquivo temporário em claro é removido no encerramento normal; ambiente de runner efêmero reduz exposição. A segurança de longo prazo depende da força/proteção da frase secreta e revisão criptográfica posterior.

O workflow `poc-backup.yml` usa `postgres:18` para corresponder ao Neon e publica **apenas o arquivo criptografado e checksum** como artifact do GitHub Actions com retenção de 90 dias. O [run 37803587635](https://github.com/danieLx77/Tickr/actions/runs/37803587635) passou; o artefato foi baixado e o checksum portátil validado fora do runner. Exclusão/rotação 7 diários + 4 semanais + 3 mensais, capacidade de 500 MB e recuperação após perda do repositório não foram validadas. Não confiar em artifacts como única cópia permanente; exclusão de workflow/repositório pode apagá-los.

## Restauração

1. Recuperar o `.dump.enc` e o `.sha256` do destino externo aprovado e verificar acesso/autenticidade do artifact.
2. Preparar banco **isolado e vazio**, com versão PostgreSQL compatível ou superior à do dump. O Neon desta PoC usa PostgreSQL 18; `pg_dump` 16 do runner falhou. O teste de restauração do artefato remoto passou em PostgreSQL 18 isolado.
3. Definir `RESTORE_DATABASE_URL` para o banco isolado e `BACKUP_PASSPHRASE` separadamente; executar `bash scripts/restore-check.sh ARQUIVO.dump.enc`.
4. O script verifica SHA-256, descriptografa em arquivo temporário e executa `pg_restore --single-transaction --exit-on-error`. Se falhar, não liberar escrita.
5. Consultar contagens e valores sintéticos, chaves/restrições e relações. No teste do artefato baixado, foram recuperados `demo`, `synthetic`, uma execução lógica concluída e as restrições de chave/check. Testar migrações aplicáveis e reconstrução de caches quando existirem.
6. Registrar data, versão de origem/destino, resultado e problemas sem copiar segredos. Repetir mensalmente em ambiente isolado quando a operação remota existir.

A política 7/4/3 e um destino independente também do GitHub ainda são pendências. Um teste de restauração não prova restaurações futuras sem exercício periódico.

## Job perdido ou falho

O job registra chave lógica e horários `scheduled_at`/`executed_at` no PostgreSQL. `python backend/job.py --recover --recover-limit 24` consulta as janelas concluídas e processa as ausentes em ordem, desde **08/10/2026 21:17 UTC**, primeiro horário de cron real comprovado. Não gera horários anteriores a esse marco. O limite configurável é por execução; o log informa `pending_remaining`, e execuções seguintes continuam pelas mais antigas. Cada conclusão é gravada em transação própria, com chave única; uma falha interrompe o lote sem concluir a janela falha. Reexecução, concorrência e lacunas acima do limite passaram em testes locais com dados sintéticos. Para execução manual controlada, usar `--key CHAVE --scheduled-at HORARIO_UTC_ISO`. Atrasos adicionais podem acumular pendências; verificar a contagem e os horários persistidos no Neon após o próximo disparo real. A validação remota desta correção ainda está pendente.

Se banco, API ou e-mail falhar: manter último estado válido, registrar falha, não enviar alerta financeiro com dados antigos, corrigir credencial/rede/cota e reexecutar a janela lógica. Uma falha de envio de e-mail não foi testada; não há garantia de entrega exatamente uma vez na PoC.
