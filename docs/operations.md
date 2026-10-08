# Operações planejadas

São procedimentos para fases futuras; nenhum provedor, backup ou job está configurado. A [Fase 00](implementation-plan.md) valida operação totalmente gratuita, remota e independente do computador pessoal.

## Agenda e recuperação

Usar calendário B3 e `America/Sao_Paulo`, incluindo feriados, horários especiais e atraso da fonte. Metas: cotações a cada 60 min durante pregão; frontend consulta backend a cada ~5 min; proventos/eventos diariamente; histórico e Ibovespa/IDIV após fechamento; empresas semanalmente; resumo às segundas 08:00 no horário de Brasília. A pontualidade depende da infraestrutura gratuita. Jobs registram início, última execução, último sucesso, período coberto, lacunas e falhas; usam idempotência, controle de concorrência, backoff exponencial e recuperação incremental. Execução perdida deve ser detectada. Evitar alertas em massa após indisponibilidade prolongada.

## Alertas e e-mail

A entrada na zona de compra é detectada apenas com cotação e DPA válidos (cotação com mais de aproximadamente 1 hora durante o pregão não gera novo alerta, limiar final a validar), por queda do preço ou aumento verificado do teto. Estado persiste no servidor. No máximo um alerta por ativo/dia; saída seguida de nova entrada pode alertar em outro dia. Troca de filtros não dispara alerta. Preferência global e por ativo pode desligar. Agrupar todas as entradas de uma sincronização em um e-mail com cotação, teto, zona, distância, DPA/configuração, fonte/horário, link e aviso de não recomendação. Registrar detecção, chave idempotente, tentativa, resposta e falha. Sem garantias verificadas do provedor, não prometer entrega exatamente uma vez.

Resumo semanal cobre segunda–domingo anterior, mesmo sem operações: valor de mercado, TWR se confiável, aportes, proventos **recebidos**, oportunidades, pagamentos nos 14 dias seguintes apenas se datas confiáveis, comparação Ibovespa/IDIV e lacunas. E-mail administrativo somente para falhas críticas ou persistentes; falha temporária aparece no painel. Se o provedor cair, reter estado para nova tentativa sem duplicar indevidamente.

## Saúde, limites e degradação

Configurações terá “Saúde do sistema” para API, banco, fontes, sincronizações, e-mail, backup e cotas. Estados: operacional, degradado, indisponível, desconhecido. Falta de informação recente não é operacional. Monitorar idade dos dados, execução perdida, capacidade do banco, cotas de API/e-mail e sucesso de backup/restauração. Se a cota gratuita apertar, reduzir frequência ou adiar trabalho não crítico, mantendo dados antigos rotulados; nunca pagar automaticamente, fabricar dados ou enviar alerta com preço antigo. Registrar causa e janela de recuperação.

## Backup, restauração e retenção

Meta: backup PostgreSQL consistente diário, criptografado antes do armazenamento externo independente, com checksum, sucesso/falha e último backup válido preservado. Rotação desejada de 7 diários, 4 semanais e 3 mensais, condicionada à capacidade gratuita validada. Chave de recuperação protegida separadamente; backup extraordinário antes de ação administrativa de alto risco quando viável. A PoC deve demonstrar destino gratuito real e restauração. Testar restauração mensal em ambiente isolado: integridade, relações, restrições, migrações, dados financeiros e reconstrução de caches. Não liberar escrita em base parcialmente restaurada. Retenção financeira permanente; logs técnicos 30 dias e histórico de sincronização 90 dias são proposta sujeita à capacidade. Exportação CSV/JSON não é backup.

Procedimento de incidente: identificar último dado/backup válido e escopo, suspender escritas inseguras ou alertas financeiros, preservar evidências, recuperar incrementalmente ou restaurar em ambiente isolado, validar integridade e caches, então reabrir escrita. Documentar perda possível e falhas. RPO/RTO concretos dependem da PoC.

## Evidência operacional da Fase 00

O [registro da PoC](poc/test-results.md) distingue backup/restauração locais de operação remota; rotinas de produção e retenção continuam pendentes.
