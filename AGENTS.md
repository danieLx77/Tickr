# Instruções para agentes — Tickr

1. Leia [README.md](README.md), [requisitos](docs/requirements.md), [plano](docs/implementation-plan.md) e os documentos específicos do módulo antes de alterar código. Consulte [ADRs](docs/adr/README.md).
2. Respeite o custo obrigatório de R$ 0, o usuário único e a Fase 00 obrigatória antes de qualquer implementação funcional. Candidatos a provedores e fontes não são integrações aprovadas.
3. Não invente requisitos, resultados de testes, dados financeiros, datas de pagamento, comportamento de APIs ou valores para lacunas. Registre incerteza e proveniência; ausência não é zero.
4. Preserve a identidade estável do instrumento, histórico financeiro, transações atômicas, idempotência e auditoria. Correções retroativas devem reconstruir dados derivados e rejeitar históricos inválidos.
5. Use `Decimal`/`NUMERIC`; não use `float` monetário nem perca precisão na API. Mudanças de fórmula exigem atualização de [regras financeiras](docs/financial-rules.md), requisitos e testes.
6. Proteja credenciais e dados pessoais: segredos fora do Git, HTTPS, Argon2id, TOTP, sessões revogáveis, autorização, CSRF e limitação de tentativas. Nunca registre segredos em logs ou exportações.
7. Use monólito modular e adaptadores para integrações. Evite complexidade sem necessidade. Não trate exploração técnica como integração de produção aprovada.
8. O fluxo escolhido é trabalho diretamente na `main`, sem PR obrigatório. Use Conventional Commits em inglês e commits coesos **somente quando autorizados**. Faça verificações locais antes de alterações relevantes; CI em push relevante bloqueia o deploy se falhar. Não desabilite testes para obter sucesso.
9. Execute os testes pertinentes, lint e verificação de tipos, e informe exatamente o que foi executado. Mantenha documentos e ADRs sincronizados com decisões implementadas; liste limitações e pendências.
10. Em futuras solicitações por fase, o Codex pode subdividir a fase e avançar após verificações automatizadas aprovadas, dependências satisfeitas e ausência de ações externas que requeiram autorização. Registre que a validação funcional manual ainda está pendente; não declare o MVP pronto sem ela.
