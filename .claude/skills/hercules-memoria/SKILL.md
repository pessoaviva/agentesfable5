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
stack.md          # perfil do projeto: frameworks, versões, deps, deploy/ambiente, contexto do time
commands.md       # comandos que comprovadamente funcionam neste projeto
architecture.md   # mapa detalhado: módulos, responsabilidades, fluxos, padrões recorrentes
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
durável (nada de diário):

- O que funcionou?
- O que falhou?
- O que não deve ser repetido?

Formato de `lessons.md` — uma seção por lição, três linhas no máximo:

```
## <data> — <tipo de tarefa>
funcionou: ... | falhou: ... | da próxima vez: ...
```

**Antes de tarefa parecida, consulte o "da próxima vez"** — é ele que muda
sua ESTRATÉGIA, não só sua memória. Aprender é adaptar a abordagem, não
acumular anotações. Comando que funcionou vai para `commands.md`; decisão
de arquitetura, para `architecture.md`.

## Análise de falha

Quando a entrega sair `parcial`/`bloqueado` por falha, ou o teto de ciclos
de correção estourar, classifique a causa ANTES de encerrar:

faltou contexto no briefing · erro externo (rede, serviço, ambiente) ·
bug seu · dependência · instrução ambígua · limitação de ferramenta

Registre em `lessons.md` com a classe. Falha da mesma classe repetida em
tarefas diferentes é o primeiro candidato a "da próxima vez".

## Padrões recorrentes do projeto

Percebeu que o projeto sempre repete uma sequência (ex.: controller →
service → repository → DTO; página → seção → componente)? Registre o
padrão em `architecture.md` e SIGA-O nas próximas criações. Detectar o
padrão uma vez é barato; redescobri-lo em toda invocação, não.

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
