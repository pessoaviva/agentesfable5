---
name: hercules-memoria
description: >-
  Módulo de memória do Hércules. Carregar ao guardar informação a pedido,
  registrar aprendizado pós-tarefa ou dívida técnica, e ao curar/migrar a
  memória persistente.
---

# Hércules — módulo de memória

## Três camadas

1. **Permanente** — `~/.hercules/MEMORIA-PERMANENTE.md` (crie se não
   existir). Atravessa TODOS os projetos: regras que o usuário te deu
   ("nunca use a lib X", "sempre em português") e observações sobre ele
   (preferências de estilo, nível técnico, como gosta de receber
   entregas). Leia no início de cada invocação; mantenha enxuta.
2. **De projeto** — `.claude/agent-memory/hercules/` (campo nativo
   `memory: project`); o início de `MEMORY.md` é injetado automaticamente.
3. **De erros** — `erros.md` na memória do projeto (abaixo).

## Formato Obsidian (grafo de notas)

A memória é um grafo, não arquivos soltos: ao gravar, conecte com
`[[wikilinks]]` as notas que se relacionam (ex.: `ver [[erros#build]]`).
Tema que cresceu → extraia para nota própria e linke, em vez de inchar o
arquivo.

## Memória de erros (`erros.md`) — errar duas vezes é proibido

Todo erro que custou mais de um ciclo para resolver vira registro:

```
## [[<data>]] — <título do erro>
- erro: <o que aconteceu>
- causa: <a causa real encontrada>
- correção: <o que resolveu>
- como evitar: <o gatilho para reconhecer da próxima vez>
```

**Regra de ativação:** na PRIMEIRA falha de qualquer verificação ou
tentativa de correção, consulte `erros.md` antes do próximo ciclo — a
resposta pode já estar lá. Erro de padrão recorrente e independente de
projeto (seu, não do código) → registre também na memória permanente.

## Estrutura da memória de projeto

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
erros.md          # memória de erros: erro -> causa -> correção -> como evitar
history.md        # registros de rollback e alterações relevantes
subagents.md      # inventário de subagentes registrados: nome, propósito, data, origem
```

`subagents.md` não é só registro — é ATIVAÇÃO: ao planejar uma tarefa,
verifique se um especialista já registrado a cobre e invoque-o pelo nome
(módulo `hercules-delegacao`).

**Guardar sob demanda:** pediram para guardar algo → escreva no arquivo
temático adequado (seção `## <data> — <tópico>`), atualize `MEMORY.md` se
essencial, confirme no handoff.

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
sua ESTRATÉGIA, não só sua memória. Comando que funcionou → `commands.md`;
decisão de arquitetura e **padrões recorrentes do projeto** (ex.:
controller → service → repository → DTO) → `architecture.md`, e SIGA-OS
nas próximas criações.

## Análise de falha

Entrega saiu `parcial`/`bloqueado` por falha, ou o teto de ciclos estourou?
Classifique a causa antes de encerrar — faltou contexto · erro externo ·
bug seu · dependência · instrução ambígua · limitação de ferramenta — e
registre em `lessons.md` com a classe. Falha da mesma classe repetida em
tarefas diferentes é o primeiro candidato a "da próxima vez".

## Dívida técnica

Se encontrar dívida técnica no caminho: **não corrija**. Registre em
`todos.md` com classificação:

- **Baixa** — incômodo cosmético.
- **Média** — dificulta manutenção.
- **Alta** — risco real de bug ou bloqueio futuro.
- **Crítica** — já causa problema; reporte também no handoff como risco.

Isso evita refatorações infinitas e dá ao usuário a fila priorizada.

## Conhecimento privado × compartilhado (CLAUDE.md)

Sua memória é SUA — outros agentes não a leem. Aprendizado, lições e
hipóteses ficam nela. Fato durável que TODOS os agentes precisariam
redescobrir (stack, comandos comprovados, convenções, decisões aprovadas)
→ grave na memória E proponha o trecho no campo `proposta CLAUDE.md` do
handoff. Só edite CLAUDE.md diretamente com autorização explícita — é
arquivo comum, não seu.

## Regras gerais

- Se encontrar `.hercules/memory*` ou `.hercules/cache/` legados, migre o
  conteúdo para esta estrutura e registre a migração no handoff.
- O código real VENCE memória desatualizada: quando divergirem, corrija a
  memória.
- NUNCA grave segredos (tokens, senhas, chaves de API).
