# Fontes externas e qualidade dos dados

Nenhuma fonte externa está aprovada para produção. Adaptadores isolam provedores das [regras financeiras](financial-rules.md). Cada dado guarda fonte, identificadores disponíveis, versão, instante observado e instante coletado; ausência não significa zero. Respostas corrigidas geram nova versão e reconciliação, sem apagar decisões manuais ou dados válidos quando a fonte falhar.

| Finalidade | Candidato e cobertura | Limitação a validar |
| --- | --- | --- |
| Proventos/JCP | Serviço público usado pelo site da B3, associado a `GetListedCashDividends`; RI das empresas e CVM/IPE para conciliação | Acesso automatizado/termos, estabilidade, pagamento ausente, data-ex não explícita, identidade do evento e classificações. |
| Cotações | brapi gratuita | Hipóteses de um ticker/chamada, ~15.000 chamadas/mês e atraso ~30 min; confirmar limites atuais e confiabilidade. |
| Preços históricos | B3 COTAHIST | Formato de largura fixa, parser/validação, preço originalmente não ajustado, disponibilidade/atualização e eventos societários. |
| Empresa/instrumento | Cadastros públicos B3 e CVM | Identidade estável, setor/BESST e mudanças de ticker. |
| Benchmarks | Séries adequadas de Ibovespa e IDIV | Calendário, base, atualização, licença e natureza de retorno total do IDIV. |

## Exploração de dividendos em 07/10/2026

Foram feitas **18 requisições pequenas** para BBDC4, CPFE3, CSMG3, PSSA3 e VIVT3, com **176 eventos** observados de 2022–2026, predominantemente dividendos e JCP. Campos vistos: valor bruto por ação, `lastDatePriorEx` (data-com), `typeStock`, `corporateAction` e `dateApproval`. A exploração não encontrou data de pagamento confiável, data-ex explícita nem ID universal estável. Esse serviço não deve ser chamado de API oficial pública garantida ou integração aprovada. A PoC de acesso e pesquisa de termos deve preceder uso automatizado em produção.

## Reconciliação e cache

Não deduplicar apenas por ticker/data-com: versões, tipo, instrumento, valor e fonte podem distinguir ou corrigir eventos. Conservar bruto, normalizado, classificação original, override, evidência e histórico de correções. Divergências relevantes pedem RI/CVM-IPE ou decisão manual auditada. Não inventar pagamento, data-ex ou recorrência; redução de capital não compõe DPA. Evento societário simples só é aplicado automaticamente após verificação; complexo requer tratamento manual. Separar `observed_at` e `fetched_at`, preços ajustados e não ajustados, e mostrar validade na interface.

Objetivos de coleta: cotações a cada 60 minutos no pregão, proventos/eventos diariamente, histórico e índices após fechamento, empresas semanalmente. Frontend consulta o backend a cada ~5 minutos; atualização manual respeita cache/cotas. Todos os intervalos dependem dos limites gratuitos. Em falha, preservar último dado com idade e estado visíveis; bloquear novo alerta financeiro com dado antigo ou insuficiente. Não usar scraping frágil sem validação, exceder termos ou acionar provedor pago automaticamente. [Operações](operations.md) define recuperação.
