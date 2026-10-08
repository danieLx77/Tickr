# Arquitetura planejada

## Decisões e limites

Monorepo, monólito modular, API REST, frontend React/TypeScript, backend Python/FastAPI e PostgreSQL são escolhas de arquitetura. Docker Compose servirá ao ambiente local. Domínio financeiro, casos de uso, apresentação e infraestrutura serão separados; adaptadores isolam fontes e e-mail. Não introduzir microsserviços. [ADRs](adr/README.md) registram a justificativa. O custo de produção é obrigatoriamente R$ 0 e a [Fase 00](implementation-plan.md) antecede código funcional.

## Componentes e fluxos

- **Frontend:** sete áreas, página de ativo, formulários, gráficos e estados de dados. Consulta apenas a API/backend, inclusive na atualização visual de ~5 minutos; não consulta provedores externos diretamente.
- **API FastAPI:** autenticação, autorização, validação, casos de uso e apresentação de dados com decimais serializados sem perda. Regras financeiras puras ficam independentes de HTTP e de provedores.
- **PostgreSQL:** registros financeiros originais, versões externas, auditoria, sessões, estado de jobs e caches derivados. Operações que mudam histórico usam transações e controle de concorrência.
- **Adaptadores:** mercado, índices, e-mail e armazenamento de backup, com proveniência, limites, timeout e falhas explícitos.
- **Jobs fora da execução serverless da API:** coleta, reconciliação, reconstrução, detecção de alertas, e-mail e backup. São idempotentes, persistem estado e retomam lacunas.

Fluxo de mercado: fonte → adaptador → validação/versão → armazenamento → cálculo derivado → API → interface. Fluxo financeiro: operação manual → transação e auditoria → reconstrução cronológica → posição/indicadores → API. Fluxo de alerta: sincronização válida → estado de transição → outbox/envio com deduplicação → registro de tentativa; entrega exatamente uma vez não é prometida. O desenho concreto da fila/outbox depende de implementação e teste.

## Segurança

Um administrador, sem cadastro público. Provisionamento inicial seguro a definir antes da Fase 02; login e-mail/senha com Argon2id, TOTP obrigatório, códigos de recuperação de uso único protegidos, sessões revogáveis no servidor por até sete dias. HTTPS, cookies `HttpOnly`/`Secure`/`SameSite` adequados, CSRF, rate limiting, autorização em todas as rotas privadas, validação de entrada, logs sem segredos e auditoria sensível. Exportações excluem credenciais, tokens, hashes, segredos TOTP e códigos de recuperação. Detalhes em [modelo](data-model.md) e [testes](test-strategy.md).

## Infraestrutura candidata e contingência

Vercel (frontend e possível API), Neon (PostgreSQL), GitHub Actions (CI e jobs) e Resend (e-mail) são **hipóteses técnicas**, não produção aprovada. A PoC precisa verificar HTTPS, persistência, cron sem computador local, domínio gratuito para e-mail, backup externo criptografado, restauração, limites, segurança, conexões serverless e custo total zero. Agendamento pontual e cotas constantes não são garantidos. Se um candidato falhar, buscar opção gratuita que preserve requisitos ou adaptar o desenho; não habilitar fallback pago. Deploy futuro somente após CI aprovada, com estado de migração e restauração verificados. [Fontes externas](data-sources.md) e [operações](operations.md) detalham riscos.

## Estado da Fase 00

O [protótipo local e sua matriz de validação](poc/README.md) ainda não comprovam hospedagem, agendamento, e-mail ou backup externo. Nenhum provedor foi aprovado.
