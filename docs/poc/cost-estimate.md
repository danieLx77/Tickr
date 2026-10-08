# Estimativa mensal de consumo

**Data:** 08/10/2026. Estimativa, não medição. `N` é o número de ativos monitorados, ainda indefinido. Considera 22 pregões/mês e 8 horas de coleta por pregão apenas como cenário; calendário e duração reais variam. Acrescentar 20% de reexecuções/falhas. Nenhum crédito promocional integra o cálculo.

| Carga | Cenário base | Com margem de 20% |
| --- | ---: | ---: |
| Sincronizações horárias de cotação | 22 × 8 = 176 jobs/mês; se uma chamada/ativo, `176N` chamadas | 212 jobs; `212N` chamadas |
| Proventos + eventos societários diários | 2 × 30 = 60 jobs; chamadas dependem da fonte | 72 jobs, sem afirmar cota externa |
| Histórico + dois índices após fechamento | 3 × 22 = 66 tarefas lógicas | 80 tarefas |
| Cadastro semanal | ~4–5 execuções | ~6 execuções |
| Resumo semanal | ~4–5 e-mails | até 6 tentativas |
| Alertas | Frequência desconhecida; testar cenários de 0, 1 e 10/dia | Até 12/dia no cenário alto |
| Backups | 30 dumps/mês | ~36 tentativas; retenção desejada 14 cópias selecionadas |
| Frontend aberto 8 h em 22 dias, consulta a cada 5 min | 2.112 ciclos de consulta | ~2.535 ciclos; multiplicar pelas chamadas de API por ciclo |

A hipótese antiga de brapi gratuita (~15.000 chamadas/mês, uma por ticker) **não foi verificada nesta PoC**. Sob essa hipótese, `212N ≤ 15.000` só até `N ≈ 70`; fontes e cache precisam reduzir chamadas, mas não há número de ativos decidido. O frontend deve consultar dados persistidos, não a brapi em cada ciclo visual.

[Vercel Hobby](https://vercel.com/docs/plans/hobby) anuncia 1 milhão de invocações, 4 CPU-h e 360 GB-h de memória/mês; as poucas milhares de leituras acima parecem plausíveis, mas tempo/CPU de endpoints, cold starts e tráfego real não foram medidos. [Neon Free](https://neon.com/blog/neon-free-plan-1-gb-per-project) anuncia 100 CU-h/mês e 1 GB/projeto. Em 0,25 CU, 400 horas ativas consumiriam a cota; 24×30 horas sempre ativas seriam 180 CU-h, acima dela. A escala para zero e conexões devem ser medidas. [GitHub Free](https://docs.github.com/en/actions/reference/limits) anuncia 2.000 min/mês para privados e 500 MB de artefatos. Hipótese: 212 jobs horários × 2 min + 36 backups × 3 min + 158 tarefas diárias/semanais × 2 min ≈ 848 min, antes de CI e retries extras; público pode ter minutos gratuitos, mas artefatos seguem sujeitos à cota. Para 14 backups retidos, a média de cada arquivo precisaria ficar abaixo de ~35 MB para caber em 500 MB sem outros artefatos. O dump sintético não representa tamanho de produção.

[Resend Free](https://resend.com/pricing) anuncia 3.000/mês e 100/dia: cenário de 10 alertas agrupados por dia + resumos caberia numericamente, mas domínio e envio real ainda não foram provados. [Vercel Cron Hobby](https://vercel.com/docs/cron-jobs/usage-and-pricing) não atende execução horária. [R2](https://developers.cloudflare.com/r2/pricing/) pode cobrar além do gratuito; não há garantia de custo zero estrito.

**Conclusão:** consumo pequeno é plausível em algumas cotas anunciadas, mas R$ 0 integral **não confirmado**. Primeiros limites prováveis: armazenamento de backup, CU-h/armazenamento Neon, chamada de cotação proporcional a `N`, e viabilidade de e-mail sem domínio. Degradação planejada: reduzir cadência não crítica, pausar importações pesadas, preservar dados válidos com idade explícita; nunca acionar plano pago ou alertar com dado antigo.
