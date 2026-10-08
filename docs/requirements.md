# Requisitos do Tickr

Esta é a referência de **escopo e aceite**. Fórmulas estão em [regras financeiras](financial-rules.md), desenho em [arquitetura](architecture.md), operação em [operações](operations.md) e pendências em [plano](implementation-plan.md). Tickr é o nome definitivo.

## Escopo e premissas

Aplicação web responsiva em português brasileiro, pessoal, para um administrador e uma carteira de ações da B3. BESST organiza Bancos, Energia, Saneamento, Seguros e Telecomunicações; **Outros** reúne as demais ações. Critérios Bazin expressam uma relação entre preço e proventos, sem recomendação automática. Custo operacional **R$ 0**, nuvem independente do computador pessoal, sem serviço ou domínio pago. Não há cadastro público, negociação, corretora ou saldo de caixa operacional completo no MVP. As fontes e provedores são candidatos a validar na Fase 00 ou antes da integração correspondente.

## Requisitos funcionais

| ID | Requisito e condição observável |
| --- | --- |
| RF-001 | Acompanhar qualquer ação da B3; exibir setor e classificação BESST/Outros, com filtros por categoria. |
| RF-002 | Watchlist manual independente da carteira; mostrar cotação, atualização, DY, DPA, teto, zona, distância e estado; ordenar oportunidades pela distância, sem juízo de qualidade. |
| RF-003 | Persistir seletores globais 12M/3A/5A e somente recorrentes/todos; aplicar a todas as telas dependentes sem gerar alertas pela troca do filtro. |
| RF-004 | Exibir proventos brutos/líquidos, data-com, data de pagamento somente se conhecida, classificação, fonte, correção e suficiência do histórico; permitir classificação manual auditável. |
| RF-005 | Registrar e aplicar eventos societários verificados, inclusive desdobramento, grupamento, bonificação e mudança de ticker; tratar casos complexos manualmente com auditoria. |
| RF-006 | Cadastrar compras/vendas manuais, inclusive históricas, com data da negociação, instrumento, quantidade, preço, taxas opcionais e observações; calcular posição, preço médio e resultados. |
| RF-007 | Registrar origem da compra como aporte, proventos ou mista com parcelas; distinguir aportes, retiradas e movimentos internos sem alterar o preço médio pela origem. |
| RF-008 | Distinguir proventos anunciados, esperados na data-com e recebidos confirmados; preservar divergência e confirmação manual em correções. |
| RF-009 | Mostrar valor de mercado, resultados realizado/não realizado, proventos, Yield on Cost e TWR quando confiável; históricos de patrimônio, aportes e comparação Ibovespa/IDIV em datas coerentes. |
| RF-010 | Detalhe do ativo com empresa, cotação, origem, preço e proventos históricos (idealmente 5–10 anos quando disponíveis), DPA, teto, zona, posição e gráficos comparáveis. |
| RF-011 | Dashboard com patrimônio, TWR, proventos, aportes, evolução, distribuição BESST/Outros, benchmarks, oportunidades e validade dos dados. |
| RF-012 | Consultar backend a cada ~5 min com app aberto; sincronizar cotações ~60 min no pregão, proventos/eventos diariamente, histórico/índices após fechamento e empresas semanalmente, sujeitos às cotas. Atualização manual controlada. |
| RF-013 | Alertar por e-mail na entrada verificada de ativo da Watchlist na zona, inclusive por DPA alterado; agrupar eventos de uma sincronização, no máximo um por ativo/dia, sem repetição até saída. Controle global e por ativo. |
| RF-014 | Resumo semanal às segundas, 08:00 em `America/Sao_Paulo`, da semana anterior (segunda–domingo), mesmo sem operações, com dados confiáveis e avisos de lacunas. |
| RF-015 | Sete áreas: Dashboard, Carteira, Watchlist, Oportunidades, Proventos, Análises e Configurações; detalhe do ativo como página própria. Temas claro/escuro/automático, acessibilidade por teclado e estados vazios/de erro. |
| RF-016 | Exportar CSV e JSON versionado, completo e estruturado, preservando decimais, datas, relações e auditoria relevante, excluindo todos os segredos. Exportação não substitui backup. |
| RF-017 | Saúde do sistema com API, banco, fontes, jobs, e-mail, backup e limites; estados operacional, degradado, indisponível ou desconhecido. |
| RF-018 | Login por e-mail/senha e TOTP obrigatório, recuperação segura, sessões revogáveis e provisionamento inicial protegido, sem cadastro público. |

## Regras de negócio de alto nível

| ID | Regra |
| --- | --- |
| RN-001 | DPA usa data-com; 12M é soma, 3A e 5A são soma de 36/60 meses dividida por 3/5. Dados insuficientes deixam indicador indisponível. |
| RN-002 | DY tradicional usa sempre DPA_12M; yield do período selecionado é indicador separado. Bazin usa DPA **líquido** selecionado / 0,06 e zona = teto × 0,95. |
| RN-003 | Verde: preço ≤ zona; amarelo: zona < preço ≤ teto; vermelho: preço > teto. Distância = (preço/zona − 1) × 100. |
| RN-004 | Somente classificação extraordinária explícita confiável ou override auditado exclui evento do filtro recorrente; redução de capital nunca compõe DPA. |
| RN-005 | JCP usa regra tributária versionada por vigência; 17,5% em 2026 é premissa pendente de verificação normativa. Nunca aplicar retroativamente de modo indiscriminado. |
| RN-006 | Compras incluem taxas no custo; venda parcial conserva custo médio remanescente e gera resultado realizado; zeragem encerra ciclo. Eventos societários podem mudar quantidade/custo. |
| RN-007 | Correção/exclusão lógica retroativa é atômica, auditável e reconstrói cronologicamente posições, custos e expectativas; rejeita venda posterior inválida e preserva recebimento confirmado. |
| RN-008 | Elegibilidade a provento depende da posição na data-com; recebimento efetivo não é sobrescrito por expectativa. |
| RN-009 | Compras, vendas e reinvestimentos são movimentos internos salvo fluxo externo registrado. TWR exige avaliações e fluxos suficientes; não apresentar aproximação como exata. |
| RN-010 | Alerta exige dados atuais (limiar inicial de aproximadamente 1 hora para cotação durante o pregão, a confirmar), transição persistida e sem disparo por troca de preferências, recuperação em massa ou mera permanência. |

## Requisitos não funcionais

| ID | Requisito |
| --- | --- |
| RNF-001 | Operação integral em nuvem por R$ 0, sem computador doméstico ligado e sem fallback pago. |
| RNF-002 | Segurança: Argon2id, TOTP, recuperação de uso único, HTTPS, cookies seguros, CSRF, rate limiting, autorização, segredos externos ao Git e logs seguros. |
| RNF-003 | Exatidão decimal, integridade transacional, auditoria e reconstrução determinística. |
| RNF-004 | Proveniência, versões e horário de observação/coleta; ausência e desatualização explícitas. |
| RNF-005 | Disponibilidade degradada quando fontes falham, preservando dados válidos e suprimindo alertas financeiros inseguros. |
| RNF-006 | Interface web responsiva e acessível em desktop e navegador móvel, em português brasileiro. |
| RNF-007 | Módulos financeiros independentes de provedores; possibilidade de substituição de adaptadores. |
| RNF-008 | Backup diário criptografado, armazenamento independente e restauração testada; política sujeita à capacidade gratuita. |

## MVP, adiamentos e aceite

O MVP cobre RF-001 a RF-018 conforme disponibilidade confiável dos dados, inclusive gráficos históricos completos, TWR e benchmarks **quando houver dados suficientes**. Falta de dados deve produzir estado indisponível visível, nunca série inventada. Não entram no MVP: importação CSV, importação/restauração JSON pela interface, múltiplos usuários/carteiras, outras classes de ativos, corretoras, ordens, PWA instalável, aplicativo nativo, tributação completa, IA/notícias, projeções avançadas, Open Finance e novos métodos de valuation. Cadastro manual retroativo permanece no MVP.

Cada módulo exige testes automatizados pertinentes, lint/tipos, evidência de execução, estados de erro e orientação de validação manual. Aceite definitivo exige validação funcional manual, segurança, integridade financeira, restauração, custo zero e requisitos críticos. Passagem automática entre fases não equivale a aceite manual. Critérios detalhados: [estratégia de testes](test-strategy.md) e [plano](implementation-plan.md).
