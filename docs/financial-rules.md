# Regras financeiras

Esta é a referência das fórmulas. Usar `Decimal` em Python e `NUMERIC` no PostgreSQL, nunca `float` para dinheiro. A API transmite decimais como strings ou representação exata equivalente. Manter precisão por ação durante o cálculo; arredondar apenas nos limites de apresentação/liquidação conforme regra da operação ou fonte, preservando o valor efetivamente liquidado. A escala e modo de arredondamento específicos por evento/fonte precisam ser validados antes da implementação.

## Proventos, DPA e Bazin

Somente dividendos e JCP elegíveis compõem DPA; redução de capital e outros eventos não compõem. A data-com determina período e elegibilidade. Um evento só sai do filtro “somente recorrentes” quando houver classificação extraordinária explícita e confiável ou override auditado. Ausência de classificação não autoriza inferência pelo valor. Datas de pagamento desconhecidas permanecem ausentes.

Para uma data de referência `t`, somar valores **líquidos por ação** com data-com nos intervalos de 12, 36 ou 60 meses anteriores, com limites temporais consistentes a definir na implementação: `DPA_12M = Σ12M`; `DPA_3A = Σ36M / 3`; `DPA_5A = Σ60M / 5`. Cobertura insuficiente torna o período indisponível, sem completar lacunas com zero. O seletor global persistido escolhe o DPA de Bazin. `DY tradicional = DPA_12M / cotação × 100`, independentemente do seletor; `yield selecionado = DPA selecionado / cotação × 100` deve ter rótulo distinto. Cotação ausente, nula ou ≤ 0 torna yields e ranking indisponíveis.

Regra de planejamento para JCP em 2026: retenção de **17,5%**, portanto `JCP líquido = JCP bruto × 0,825` (exemplo: R$ 1,00 bruto → R$ 0,825 líquido por ação antes da liquidação). A alíquota, vigência, evento aplicável e arredondamento exigem verificação normativa; regras versionadas impedem recálculo indevido de eventos antigos. Dividendos brutos e líquidos permanecem campos distintos conforme tratamento aplicável.

`Preço-teto = DPA líquido selecionado / 0,06`; `zona = preço-teto × 0,95`; `distância (%) = (cotação / zona − 1) × 100`. Exemplo: DPA de R$ 2,40 → teto R$ 40,00 → zona R$ 38,00; preço R$ 36,10 → distância −5%, **verde**. Preço R$ 38,00 é verde; R$ 39,00, amarelo; acima de R$ 40,00, vermelho. Zona ausente ou ≤ 0 impede distância e classificação. Distância mais negativa é mais favorável no ranking, sem significar qualidade. `Yield on Cost = DPA_12M / preço médio de aquisição × 100`; preço médio ausente/zero deixa o índice indisponível. Com DPA R$ 2,40 e preço médio R$ 30,00, YoC = 8%; DY sobre cotação R$ 40,00 = 6%.

## Operações, custo e resultados

Na compra, `custo acrescido = quantidade × preço unitário + taxas de compra aplicáveis`; `preço médio = custo total da posição / quantidade`. Exemplo: 10 ações a R$ 20 + R$ 2 de taxas → custo R$ 202 e média R$ 20,20. Outra compra de 10 a R$ 30 sem taxa → custo R$ 502 para 20 ações e média R$ 25,10. A origem aporte/provento/mista não altera esse custo.

Na venda parcial, baixar `quantidade vendida × preço médio anterior` do custo da posição; `resultado realizado = quantidade vendida × preço de venda − taxas de venda − custo baixado`. Exemplo: vender 5 das 20 ações anteriores a R$ 28 com R$ 1 de taxa → receita líquida R$ 139, custo baixado R$ 125,50, resultado R$ 13,50; 15 ações mantêm média R$ 25,10. `resultado não realizado = valor de mercado da posição − custo remanescente`, sujeito a cotação válida. Venda total zera custo e encerra ciclo; nova compra inicia outro ciclo. Desdobramento/grupamento altera quantidade e custo unitário sem criar retorno por si; bonificação requer custo fiscal validado, não custo zero presumido. Mudança de ticker preserva instrumento.

`provento esperado = quantidade elegível na data-com × valor líquido por ação`. Exemplo: 15 ações × R$ 0,80 = R$ 12 esperados. Recebimento confirmado pode divergir e permanece separado. Correção posterior de operação recompõe expectativa, mas não sobrescreve o recebido.

## Patrimônio, TWR e índices

`valor de mercado = Σ(quantidade × cotação válida correspondente)`. Fluxos externos (aportes e retiradas) diferem de compras, vendas, proventos e reinvestimentos internos. TWR é a métrica percentual principal; exige avaliações datadas nas fronteiras de fluxos externos e encadeamento dos subperíodos. O modelo interno mínimo de fluxos/caixa técnico para conciliar vendas e dividendos sem módulo de conta-corrente continua **pendência técnica**. Até validá-lo, não usar uma fórmula simplificada que conte compras como aportes ou vendas como retiradas, nem exibir TWR incompleto como exato. Retorno total, variação e patrimônio precisam de rótulos que explicitem a base efetivamente calculada.

Comparar TWR da carteira a Ibovespa e IDIV em base 100, com mesma data inicial/final, calendário e dados suficientes; IDIV é índice de retorno total. Períodos: 1, 3 e 6 meses; 1, 3 e 5 anos; desde o início. Ajustes de eventos societários e identificação de preços ajustados/não ajustados são obrigatórios para séries comparáveis. Lacuna de cotação, fluxo, evento ou índice torna o trecho indisponível ou explicitamente incompleto.

## Validação de extremos

Testar preço/denominador zero, histórico insuficiente, ausência de provento comprovada versus cobertura desconhecida, JCP em vigências diferentes, evento corrigido, desdobramento/grupamento, bonificação com custo, venda além da posição, correção retroativa inválida, cotação antiga e exportação decimal. [Cenários completos](test-strategy.md).
