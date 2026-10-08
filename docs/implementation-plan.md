# Plano de implementação e registro de validações

A documentação está consolidada e a PoC local da Fase 00 está em andamento; seu aceite remoto permanece pendente ([evidências](poc/README.md)). **Fase 00 é obrigatória antes de qualquer implementação funcional do MVP.** Uma solicitação futura cobre uma fase completa; o Codex pode subdividi-la internamente. Avanço automático entre fases exige dependências e verificações automatizadas aprovadas, nenhuma falha crítica e autorização para ações externas sensíveis quando necessária. A validação funcional manual segue pendente até execução explícita. Esta documentação não autoriza implementar nenhuma fase agora.

| Fase | Entrada e entregáveis | Saída e verificação |
| --- | --- | --- |
| **00 — PoC gratuita** | Documentação atual. Frontend HTTPS mínimo, FastAPI remoto, PostgreSQL persistente, autenticação básica de viabilidade, job remoto, e-mail real sem domínio pago, backup criptografado externo e restauração. | Relatório de custo R$ 0, cotas, falhas, segurança, execução sem PC local, evidências de envio/restauração e escolha fundamentada de provedores. Sem aprovação da PoC, não iniciar fases funcionais. |
| **01 — Fundação** | 00 aprovada. Monorepo, frontend/backend, Docker Compose, PostgreSQL, migrações, configuração, qualidade, testes iniciais e CI. | Ambiente local reproduzível; migrações e testes iniciais, lint/tipos e CI passam. |
| **02 — Segurança** | 01. Admin, provisionamento, login, Argon2id, TOTP, recuperação, sessões revogáveis, CSRF, rate limiting e autorização. | Testes de autenticação, abuso, sessão e segredo passam; validação manual registrada. |
| **03 — Mercado** | 01/02 e condições de fonte verificadas. Empresas, instrumentos, ticker histórico, adaptadores, cotações, preços, proventos, eventos, índices e proveniência. | Testes de parser/adaptador, migração, reconciliação, falha e idempotência; lacunas visíveis. |
| **04 — Financeiro** | 03 e vigência de JCP/TWR/eventos tratadas. Carteira, operações, fluxos, eventos, proventos, DPA, DY, Bazin, TWR e reconstrução. | Matriz financeira, ≥80% domínio, transações, correções, precisão e períodos incompletos verificados. |
| **05 — Interface e análises** | 02–04. Sete áreas, detalhe de ativo, dashboard, gráficos, benchmarks, temas e responsividade. | Testes de componentes/E2E, acessibilidade, dados incompletos e validação móvel. |
| **06 — Alertas e automação** | 03–05 e e-mail/job validados. Watchlist, transição, agrupamento, deduplicação, resumo e recuperação. | Testes de idempotência, falha de envio, preferências e ausência de disparo por filtro. |
| **07 — Consolidação** | 01–06. Exportação, auditoria/painel de saúde, backup/restauração operacional, E2E, revisão de segurança/custo e implantação. | CI, E2E, restauração, R$ 0 e validação funcional manual; só então considerar MVP pronto. |

Segurança, integridade, auditoria e testes são transversais e entram desde a fase em que forem necessários; a Fase 07 consolida, não adia sua existência. Desenvolvimento diretamente na `main`, sem PR obrigatório, Conventional Commits em inglês, testes locais antes de mudanças relevantes e CI em push relevante. Como CI roda após push, bloqueia o deploy de revisão reprovada. Não desligar verificações para obter aprovação artificial.

## Registro rastreável

Legenda: **Decisão confirmada** = requisito estabelecido; **hipótese técnica** = candidato; **pendência** = validação necessária; **risco conhecido** = impacto possível; **fora do escopo** = adiamento deliberado. Candidatos de infraestrutura e fonte nunca são tratados como decisão confirmada. As pendências abaixo devem ser fechadas com evidência na fase indicada; se uma resposta mudar requisito, atualizar [requisitos](requirements.md), documento especializado e ADR.

| ID | Tipo e questão | Quando/evidência esperada |
| --- | --- | --- |
| P-01 | Pendência: permissão, termos e estabilidade da automação de dividendos B3 | 00/03; termos e teste de acesso. |
| P-02 | Hipótese/risco: cotas e estabilidade da brapi gratuita | 00/03; limites medidos/termos. |
| P-03 | Pendência: disponibilidade e atualização B3/COTAHIST | 03; amostra histórica e parser validado. |
| P-04 | Pendência: reconciliação/recorrência confiável dos proventos | 03; casos divergentes com RI/CVM. |
| P-05 | Pendência: vigência e aplicação normativa de JCP, inclusive 17,5% em 2026 | Antes de 04; fonte normativa e testes versionados. |
| P-06 | Hipótese: hospedagem gratuita adequada de FastAPI/Vercel ou alternativa | 00; API remota e limites. |
| P-07 | Hipótese: envio Resend sem domínio pago ou alternativa | 00; envio real e termos. |
| P-08 | Risco: agendamentos gratuitos atrasarem/falharem | 00; job remoto, retomada e lacunas. |
| P-09 | Risco: capacidade/conexões gratuitas do PostgreSQL/Neon | 00; persistência, carga e limites. |
| P-10 | Pendência: destino externo independente e gratuito de backups | 00; backup criptografado e custo. |
| P-11 | Pendência: restauração isolada e proteção separada da chave | 00/07; teste de restauração. |
| P-12 | Pendência: TWR sem módulo completo de caixa; definir caixa técnico/fluxos e fronteiras | Antes de 04; modelo e casos numéricos verificados. |
| P-13 | Pendência: bonificação e demais eventos societários complexos, custo fiscal e ajustes | Antes de 04; regras e exemplos. |
| P-14 | Hipótese: retenção 30/90 dias e histórico de mercado caberem na cota | 00/07; projeção e medição. |
| P-15 | Risco: garantias de envio/deduplicação de e-mail | 00/06; falhas/retries, sem promessa de exatamente uma vez. |
| P-16 | Pendência: limites exatos das janelas e critério de cobertura do histórico, escala/arredondamento por fonte | Antes de 04; especificação e testes. |
| P-17 | Pendência: regras de preço ajustado e comparação de séries | 03/04; amostras com eventos. |
| P-18 | Pendência: limiar de cotação antiga, estado inicial e transição após indisponibilidade | 03/06; política e testes, sem alertas inseguros. |
| P-19 | Pendência: provisionamento e recuperação inicial seguros do admin | 02; procedimento e testes. |

Fora do escopo: importação CSV/JSON pela interface, PWA instalável, app nativo, multiusuário, multicarteira, ordens/corretoras, tributação pessoal completa e projeções avançadas. A ausência de solução gratuita adequada em 00 bloqueia a implantação planejada; não autoriza custo positivo.
