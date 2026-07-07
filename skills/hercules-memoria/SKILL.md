---
name: hercules-memoria
description: >-
  Módulo de memória do Hércules. Carregar ao guardar informação a pedido,
  registrar aprendizado pós-tarefa ou dívida técnica, e ao curar/migrar a
  memória persistente.
---

# Hércules — módulo de memória

A memória vive em `.claude/agent-memory/hercules/` (campo nativo
`memory: project`). O início de `MEMORY.md` é injetado automaticamente a
cada invocação.

## Estrutura

- **`MEMORY.md` é o índice curado.** Mantenha-o enxuto (é truncado em ~200
  linhas): stack detectada, comandos comprovados, mapa resumido do projeto
  e ponteiros para os arquivos temáticos.
- **Arquivos temáticos**, criados quando houver conteúdo:

```
stack.md          # frameworks, versões, dependências principais
commands.md       # comandos que comprovadamente funcionam neste projeto
architecture.md   # mapa detalhado: módulos, responsabilidades, fluxos
preferences.md    # preferências do usuário (paleta, estilo, convenções)
todos.md          # pendências combinadas + dívida técnica classificada
bugs.md           # bugs conhecidos e estado de cada um
api.md            # contratos de API, endpoints, formatos combinados
lessons.md        # aprendizado pós-tarefa: o que funcionou/falhou
history.md        # registros de rollback e alterações relevantes
subagents.md      # inventário de subagentes registrados: nome, propósito, data, origem
```

## Guardar sob demanda

Quando pedirem para **guardar** algo: escreva no arquivo temático adequado
(seção `## <data> — <tópico>`), atualize o índice em `MEMORY.md` se for
essencial, e confirme no handoff.

## Aprendizado pós-tarefa (tarefas médio+)

Ao concluir, responda internamente e registre em `lessons.md` APENAS o
durável (1-3 linhas, nada de diário):

- O que funcionou?
- O que falhou?
- O que não deve ser repetido?

Comando que funcionou vai para `commands.md`; decisão de arquitetura, para
`architecture.md`. É isso que torna a próxima invocação mais barata.

## Dívida técnica

Se encontrar dívida técnica no caminho: **não corrija**. Registre em
`todos.md` com classificação:

- **Baixa** — incômodo cosmético.
- **Média** — dificulta manutenção.
- **Alta** — risco real de bug ou bloqueio futuro.
- **Crítica** — já causa problema; reporte também no handoff como risco.

Isso evita refatorações infinitas e dá ao usuário a fila priorizada.

## Conhecimento privado × compartilhado (CLAUDE.md)

Sua memória é SUA — os outros agentes e o orquestrador não a leem. Ao
gravar, classifique:

- **Privado** (fica na memória): seu aprendizado, suas lições, seu
  histórico, hipóteses ainda não confirmadas.
- **Compartilhado** (pertence ao `CLAUDE.md` do projeto, que todos leem):
  stack e comandos comprovados, convenções, decisões de arquitetura
  aprovadas — fatos duráveis que qualquer agente precisaria redescobrir.

Para o compartilhado: grave na sua memória E **proponha** o trecho para o
CLAUDE.md no campo `proposta CLAUDE.md` do handoff. Só edite CLAUDE.md
diretamente se a tarefa autorizar de forma explícita — é arquivo comum, não
seu.

## Regras gerais

- Se encontrar `.hercules/memory*` ou `.hercules/cache/` legados, migre o
  conteúdo para esta estrutura e registre a migração no handoff.
- O código real VENCE memória desatualizada: quando divergirem, corrija a
  memória.
- NUNCA grave segredos (tokens, senhas, chaves de API).
