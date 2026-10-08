# Modelo conceitual de dados

O modelo abaixo é conceitual, não uma prescrição de tabelas. A implementação deverá justificar agregações e separações. Registros originais financeiros são a fonte de verdade; posições e indicadores são derivados. Consulte [regras financeiras](financial-rules.md).

| Grupo | Conceitos e atributos essenciais | Relações e invariantes |
| --- | --- | --- |
| Identidade | Administrador, hash de senha, configuração TOTP protegida, códigos de recuperação, sessão revogável | Um administrador; sessão tem expiração ≤ 7 dias e revogação; segredos fora de exportações. |
| Mercado | Empresa, instrumento com ID estável, ticker com vigência, setor/BESST, cotação, preço histórico, índice | Ticker é rótulo temporal, nunca chave conceitual do instrumento; `observed_at` difere de `fetched_at`; identificar ajustes de preço. |
| Carteira | Carteira única, compra/venda, data de negociação, quantidade, preço unitário, taxas, observação, revisão/exclusão lógica | Operações referenciam instrumento; quantidade/preço válidos; não permitir venda além da posição cronológica. |
| Fluxos | Aporte/retirada externa, origem da compra (aporte/provento/mista), parcelas, recurso de venda, reinvestimento, caixa técnico se necessário | Não deduzir aporte da compra nem retirada da venda; parcelas da origem devem reconciliar com o financiamento registrado. |
| Proventos | Evento anunciado, tipo, valor bruto, data-com, pagamento opcional, recorrência, versão/proveniência, expectativa e recebimento confirmado | Elegibilidade pela posição na data-com; confirmação/override manual separado do evento de origem e imune a reimportação. |
| Eventos | Desdobramento, grupamento, bonificação, mudança de ticker e outros, data efetiva, fator, custo fiscal quando conhecido, fonte, aplicação | Idempotência por identidade/versionamento; evento complexo incerto exige tratamento manual auditado. |
| Produto | Watchlist, preferência global, preferências de alerta, estado de zona, detecção, envio e tentativa de e-mail | Chave de deduplicação por ativo/dia e evento; mudança de filtro não gera entrada. |
| Operação | Fonte/versão bruta relevante, reconciliação, job e última execução/sucesso, auditoria, backup, avaliação datada, cache/snapshot | Origem, versão, status, chave idempotente e timestamps; avaliações têm qualidade e cobertura explícitas. |

## Integridade e histórico

IDs estáveis identificam instrumento, operação e evento; uma chave natural parcial (ticker + data-com) não identifica provento universalmente. Guardar revisões de fonte e decisões de reconciliação, não sobrescrever fatos silenciosamente. Correção/exclusão lógica de operação cria trilha de autor, motivo e instante; em transação atômica, reexecuta a sequência afetada por data da negociação e ordem determinística, verifica posições futuras, recalcula custo/resultado e proventos esperados, invalida caches e só confirma se tudo for consistente. Conflito de concorrência deve rejeitar uma das escritas e explicar o conflito. Recebimentos confirmados ficam intactos, com divergência exibida.

Cache/snapshot derivado carrega versão das origens e dos parâmetros; mudança relevante invalida. Reconstrução simples pode ser síncrona; histórica extensa, assíncrona com estado visível, sem exibir cache antigo como atual. Jobs e eventos aplicados usam chaves idempotentes e restrições únicas apropriadas. Valor monetário usa PostgreSQL `NUMERIC` e API decimal sem perda.

## Retenção e portabilidade

Preservar permanentemente operações, fluxos, recebimentos, eventos aplicados, correções e auditoria financeira. Proposta inicial, sujeita à capacidade gratuita: logs técnicos 30 dias e histórico detalhado de sincronização 90 dias. Manter dados normalizados de mercado necessários aos cálculos, evitando arquivos brutos grandes no PostgreSQL. Exportar CSV para análise e JSON com versão de esquema, IDs, relações, decimais/datas íntegros, configurações não sensíveis e auditoria relevante. Exportação não substitui backup, e importação/restauração pela interface está fora do MVP.
