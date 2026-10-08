# Procedimentos de backup e recuperação da PoC

Estes comandos são para **dados sintéticos** e ambiente controlado. Não há destino externo aprovado. Nunca salvar `DATABASE_URL`, `BACKUP_PASSPHRASE` ou dumps em Git/logs. Fornecer segredos por gerenciador de ambiente/serviço, não pelo chat. A chave deve ficar separada do artefato. Não usar o banco principal como destino de restauração.

## Backup e integridade

Com cliente `pg_dump` compatível com o servidor de origem e destino, definir `DATABASE_URL`, `BACKUP_PASSPHRASE` e `BACKUP_OUTPUT_DIR` no ambiente e executar `bash scripts/backup.sh`. O script cria dump customizado consistente, criptografa com OpenSSL AES-256-CBC/PBKDF2 (250.000 iterações), grava SHA-256 do arquivo criptografado e verifica o checksum. O arquivo temporário em claro é removido no encerramento normal; ambiente de runner efêmero reduz exposição. A segurança de longo prazo depende da força/proteção da frase secreta e revisão criptográfica posterior.

O workflow `poc-backup.yml` propõe upload **apenas do arquivo criptografado e checksum** como artifact do GitHub Actions com retenção de 90 dias. Upload externo, download, exclusão/rotação 7 diários + 4 semanais + 3 mensais e capacidade de 500 MB ainda não foram validados. Não confiar em artifacts como única cópia permanente; exclusão de workflow/repositório pode apagá-los. Confirmar acesso restrito, política de retenção e barreira de gasto antes do uso real.

## Restauração

1. Recuperar o `.dump.enc` e o `.sha256` do destino externo aprovado e verificar acesso/autenticidade do artifact.
2. Preparar banco **isolado e vazio**, com versão PostgreSQL compatível ou superior à do dump. No teste local, ferramentas 17 falharam contra servidor 16 e passaram contra 17.
3. Definir `RESTORE_DATABASE_URL` para o banco isolado e `BACKUP_PASSPHRASE` separadamente; executar `bash scripts/restore-check.sh ARQUIVO.dump.enc`.
4. O script verifica SHA-256, descriptografa em arquivo temporário e executa `pg_restore --single-transaction --exit-on-error`. Se falhar, não liberar escrita.
5. Consultar contagens e valores sintéticos, chaves/restrições e relações. No teste local, `demo=synthetic` e uma execução lógica foram recuperados. Testar migrações aplicáveis e reconstrução de caches quando existirem.
6. Registrar data, versão de origem/destino, resultado e problemas sem copiar segredos. Repetir mensalmente em ambiente isolado quando a operação remota existir.

A política 7/4/3 e o destino gratuito independente ainda são pendências. Backup diário gerado não prova restauração futura sem teste periódico.

## Job perdido ou falho

O job registra chave lógica e horários `scheduled_at`/`executed_at` no PostgreSQL. `python backend/job.py --recover-hours 3` enumera as três janelas horárias esperadas mais recentes e insere apenas as ausentes por chave única. Reexecução é segura contra duplicação lógica no banco. Para recuperação manual controlada, usar `--key CHAVE --scheduled-at HORARIO_UTC_ISO`. O limite máximo é 24 janelas por invocação; indisponibilidade maior exige planejamento manual e eventual ampliação validada. Atraso do GitHub pode deixar janelas pendentes até a execução seguinte, e workflow público pode ser desativado após 60 dias sem atividade. Conferir histórico no Actions e estado no banco; não inferir saúde de ausência de erro recente.

Se banco, API ou e-mail falhar: manter último estado válido, registrar falha, não enviar alerta financeiro com dados antigos, corrigir credencial/rede/cota e reexecutar a janela lógica. Uma falha de envio de e-mail não foi testada; não há garantia de entrega exatamente uma vez na PoC.
