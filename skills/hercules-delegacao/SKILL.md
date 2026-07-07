---
name: hercules-delegacao
description: >-
  Módulo de delegação do Hércules. Carregar ao considerar criar
  sub-subagentes: critérios de custo/benefício, regras de escopo e decisão
  de descartar ou registrar o subagente criado.
---

# Hércules — módulo de delegação

Sub-subagentes são criados pela ferramenta **Agent** (o nome antigo `Task`
é alias). Requer Claude Code v2.1.172+; a profundidade de aninhamento é
limitada pela plataforma — não conte com mais de um nível abaixo de você.

## Critérios (avalie explicitamente antes de delegar)

- **tempo estimado** — a tarefa compensa o overhead de contexto?
- **dependências** — as unidades são realmente independentes?
- **paralelismo** — rodar em paralelo traz ganho real?
- **complexidade** — exige especialidade que você não tem no contexto
  (inclusive as áreas fora da sua especialidade: ML, infraestrutura,
  compiladores...)?

**Se houver ganho real, delegue. Caso contrário, execute sozinho.**
É PROIBIDO criar sub-subagente para tarefa resolvível em 1 chamada direta.

## Regras de execução

- Escopo fechado: os arquivos exatos que pode tocar e o formato de retorno
  esperado.
- Repasse as regras invioláveis do núcleo (segurança, prioridades) no
  prompt do sub-subagente.
- Consolide os retornos e assuma a responsabilidade pelo resultado final —
  o orquestrador só vê o SEU handoff.

## Decisão pós-tarefa (nunca promoção automática)

Ao terminar, decida explicitamente e informe no handoff:

- **descartar** — padrão para tarefas pontuais; ou
- **registrar** como subagente reutilizável em `.claude/agents/<name>.md`,
  com `name`, `description` (gatilho claro), `tools` (lista mínima — nunca
  acesso total) e system prompt. Registre apenas se o padrão de tarefa
  tende a se repetir no projeto.

## Modelo de registro

```markdown
---
name: <identificador-unico>
description: <quando o orquestrador deve invocar este subagente>
tools: <lista mínima necessária>
---
<system prompt: comportamento, modo de raciocínio, regras de economia>
```
