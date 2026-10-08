# Estratégia de testes e aceite

## Camadas e ferramentas

Domínio financeiro: testes unitários com Pytest e `Decimal`, cobrindo propriedades e limites; mínimo **80% de cobertura no domínio**, além de todos os cenários críticos. Outros módulos exigem testes relevantes sem meta global uniforme. Integração: FastAPI/HTTPX, PostgreSQL real isolado, migrações Alembic, restrições, transações, sessões, auth, jobs e adaptadores com respostas simuladas, timeouts e falhas. Frontend: Vitest e React Testing Library para componentes/estados; Playwright para fluxos E2E. Qualidade: Ruff, Pyright, ESLint, Prettier, auditoria de dependências e CI GitHub Actions. Cobertura numérica não substitui comportamento correto.

## Matriz financeira obrigatória

1. Compra simples; 2. compra com taxas; 3. múltiplas compras/média ponderada; 4. venda parcial; 5. venda total; 6. recompra após zeragem; 7. resultados realizado/não realizado; 8. desdobramento; 9. grupamento; 10. bonificação e custo; 11. mudança de ticker; 12. posição na data-com; 13. provento anunciado corrigido; 14. recebimento manual preservado; 15. JCP bruto/líquido por vigência; 16. DPA 12M/3A/5A; 17. filtro de recorrência; 18. histórico insuficiente; 19. teto Bazin; 20. zona; 21. ranking; 22. Yield on Cost; 23. mudança de filtros sem alerta; 24. correção retroativa válida; 25. inválida; 26. sincronização idempotente; 27. falha na reconstrução; 28. TWR com aportes/reinvestimentos; 29. benchmark alinhado; 30. exportação sem perda decimal.

Usar exemplos de [regras financeiras](financial-rules.md) como casos de expectativa, e acrescentar denominadores inválidos, cotação antiga, datas ausentes, preços ajustados/não ajustados e concorrência. JCP de 2026 só vira expectativa normativa após validação; até lá o teste comprova a regra versionada configurada, não uma conclusão legal.

## Integração, E2E e segurança

Testar PostgreSQL real em isolamento: migração reversível quando aplicável, unicidade/idempotência, soft delete, reconstrução atômica, retenção de recebido confirmado e conflito concorrente. Adaptadores externos são simulados em CI; condições reais só em PoC autorizada. E2E: login/TOTP, compra, venda, correção, carteira, Watchlist, Oportunidades, Configurações, exportação, estados vazios, erro, dados incompletos e uso móvel. Segurança: autorização em rotas, CSRF, rate limiting, sessão expirada/revogada, recuperação de uso único, segredo fora de logs/exportação, headers/cookies e HTTPS na implantação.

## Aceite por módulo e fase

Mercado exige proveniência e desatualização; financeiro exige reconciliação, testes da matriz e precisão; alertas exigem transição, deduplicação e falha de envio; interface exige estados e acessibilidade; operações exigem backup com restauração demonstrada. Cada fase passa testes aplicáveis, lint/tipos e registra evidência, limitações e instruções para validação funcional manual. CI aprovada pode permitir progressão automática conforme [plano](implementation-plan.md), mas não é aceite manual. MVP só pode ser declarado pronto após validação funcional, segurança, custo zero, integridade financeira, restauração e requisitos críticos.
