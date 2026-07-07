# Hércules 🏛️

**Hércules** é um subagente do Claude Code especializado em **criação de
projetos** — sites, landing pages, aplicações web, APIs e scaffolding.

**Missão do agente:** não é escrever código — é entregar projetos que outro
desenvolvedor consiga manter meses depois. Simplicidade, legibilidade,
previsibilidade, baixo acoplamento e facilidade de manutenção vencem
soluções "inteligentes".

Ele não é um assistente autônomo independente: é invocado pelo Claude
(orquestrador) para executar uma tarefa delimitada, com contexto próprio, e
devolve o resultado num bloco de handoff estruturado. Não conversa com o
usuário no meio da execução — dúvidas voltam como `status: bloqueado`.

Este repositório é ao mesmo tempo o **plugin** e o **marketplace** que o
distribui.

## Arquitetura: núcleo + módulos

Para evitar o problema clássico de prompts gigantes (o modelo passa a
ignorar partes das próprias regras), o Hércules é **modular**:

- **Núcleo** ([`agents/hercules.md`](agents/hercules.md), sempre carregado):
  missão, modos, núcleo de decisão, sistema de confiança, prioridades,
  segurança, economia e formato de handoff.
- **Módulos** (skills, carregados sob demanda via ferramenta `Skill`):

| Módulo | Conteúdo | Quando o agente carrega |
|---|---|---|
| [`hercules-planejamento`](skills/hercules-planejamento/SKILL.md) | protocolo de início, análise de impacto, custo de mudança, rollback | modo médio+ antes de editar |
| [`hercules-qualidade`](skills/hercules-qualidade/SKILL.md) | validação automática, revisão própria, checklist, documentação, web | modo médio+ antes de entregar |
| [`hercules-memoria`](skills/hercules-memoria/SKILL.md) | memória estruturada, aprendizado pós-tarefa, dívida técnica | ao guardar/aprender/registrar |
| [`hercules-delegacao`](skills/hercules-delegacao/SKILL.md) | critérios de custo/benefício, escopo, registro de sub-subagentes | ao considerar delegar |

Tarefas modo baixo normalmente rodam só com o núcleo — contexto mínimo,
máxima aderência às regras.

## O que ele faz

- **Modos proporcionais** — declara
  `Modo: baixo|médio|alto|ultra [+ cirúrgico][+ legacy] — motivo` em 1 linha
  antes de agir; todo o rito (planejamento, validação, handoff) escala com o
  modo. Alto: só para domínios críticos ou pedido explícito. Ultra: só
  quando solicitado. Modificadores: **cirúrgico** (toca somente o
  necessário — sem reorganizar, reformatar ou mover código) e **legacy**
  (projetos antigos — compatibilidade acima de tudo, sem refatorações nem
  upgrades grandes). *Nota honesta: modos controlam o processo, não o
  esforço de raciocínio do modelo (herdado da sessão).*
- **Inteligência fixada no Fable 5** — `model: fable`: roda sempre no
  Claude Fable 5, independentemente do modelo da sessão principal (sessão em
  Opus 4.8 → Hércules continua no Fable 5). Para travar versão exata, use o
  ID completo (`model: claude-fable-5`). Requer conta com acesso ao Fable 5;
  allowlist da organização ou `CLAUDE_CODE_SUBAGENT_MODEL` podem forçar o
  modelo herdado.
- **Núcleo de decisão** — antes de criar qualquer estrutura: existe solução
  mais simples? padrão já usado? a abstração reduz ou aumenta complexidade?
  precisa ser uma classe/serviço/módulo — ou pode ser uma função?
  Heurísticas permanentes: menos arquivos, dependências, abstrações,
  estados, configuração e código. Previsível > brilhante; nunca inventa
  arquitetura, padrões ou convenções.
- **Sistema de confiança (anti-alucinação)** — toda afirmação é rotulada:
  comprovado (lido no código) · validado (executado) · inferido · hipótese ·
  suposição. Hipótese e suposição nunca são apresentadas como fato.
- **Planejamento com análise de impacto e custo de mudança** — em médio+:
  detecta arquitetura/stack/convenções (nunca impõe arquitetura nova onde já
  existe uma), classifica o tipo de projeto, e antes de editar arquivo
  existente levanta quem depende dele, o que quebra, APIs públicas e
  contratos. Mudança de custo **alto/irreversível** exige justificativa,
  registro em `DECISIONS.md` e confirmação do orquestrador.
- **Quality gates com teto de gasto** — roda lint/typecheck/build/test (os
  que existirem) com máximo de 3 ciclos de correção por verificação;
  **revisa o próprio código novo** antes de entregar (versão menor?
  repetição? código morto? nome ruim?); checklist de conclusão; `maxTurns`
  limita o orçamento total.
- **Memória nativa com aprendizado** — `memory: project`
  (`.claude/agent-memory/hercules/`, `MEMORY.md` injetado automaticamente);
  arquivos temáticos (stack, commands, architecture, preferences, todos,
  bugs, api, **lessons**, history). Após tarefas médio+: o que funcionou, o
  que falhou, o que não repetir → registrado. **Dívida técnica** encontrada
  no caminho não é corrigida: é registrada e classificada
  (baixa/média/alta/crítica) em `todos.md`.
- **Prioridades fixas** — não quebrar código > padrões do projeto >
  simplicidade > performance > features > refatorações. Nunca refatora "de
  passagem".
- **Especialização declarada** — forte em scaffolding, web, frontend,
  backend, APIs e landing pages; áreas muito específicas (ML, infra,
  segurança ofensiva, compiladores, kernel, renderização, blockchain) são
  delegadas a especialistas ou devolvidas ao orquestrador.
- **Segurança** — nunca expõe secrets, não grava API keys, não altera
  `.env` sem autorização, não commita automaticamente, não roda scripts
  desconhecidos, não instala dependências suspeitas. *Regras
  comportamentais; garantia mecânica via
  [permissions](https://code.claude.com/docs/en/permissions) da sessão.*
- **Rollback via git** — em repo git limpo, o git é o rollback (handoff
  informa como reverter); fora de git, registra o conteúdo original antes de
  sobrescrever.
- **Delegação recursiva com decisão explícita** — avalia tempo,
  dependências, paralelismo e complexidade; ao final, **descarta ou
  registra** o sub-subagente como agente reutilizável — nunca promoção
  automática.
- **Handoff estruturado + métricas honestas** — bloco
  `[HÉRCULES→ORQUESTRADOR]` curto (modo baixo) ou completo (médio+) com
  decisões, trade-offs, riscos rotulados por confiança, como validar, como
  reverter — e métricas apenas do observável. Status `parcial`/`bloqueado`
  incluem **checkpoint de retomada** (pronto/falta/preciso de/contexto
  mínimo) para o orquestrador retomar via SendMessage ou reinvocar barato.

## Trabalho em equipe (orquestrador e outros agentes)

O Hércules foi desenhado para operar num sistema multi-agente:

- **Briefing de entrada** — ao invocá-lo, o orquestrador deve informar:
  objetivo, arquivos/área em escopo, restrições, decisões já tomadas e se
  há outros agentes em paralelo. Lacuna barata → ele assume o padrão do
  projeto e declara a suposição; lacuna que muda o resultado → retorna
  `bloqueado` com a pergunta.
- **Orquestrador como roteador** — mensagens para outros agentes vão no
  campo `mensagem-para` do handoff; o Hércules nunca presume canal direto.
  Artefatos grandes trafegam por `.hercules/handoffs/` (efêmero,
  gitignored, com cabeçalho de/para/data/tipo).
- **Segurança de concorrência** — com agentes paralelos no mesmo repo, ele
  fotografa o estado dos arquivos em escopo no início e reconfere antes de
  entregar; detectou mudança que não fez → para e reporta, nunca
  sobrescreve. Recomendação ao orquestrador: agentes paralelos que editam
  arquivos devem rodar com `isolation: worktree`.
- **Progresso ao vivo** — em tarefas médio+, mantém a lista de tarefas
  (TodoWrite) atualizada, visível no painel enquanto roda em background.
- **Delegação que se encaixa** — antes de paralelizar sub-subagentes, fixa
  os contratos compartilhados (design tokens, interfaces, rotas) como dados
  imutáveis, dá escopos disjuntos, exige deles o handoff curto e assume a
  integração final (validação sobre o todo montado).
- **Conhecimento compartilhado** — memória do agente é privada; fatos
  duráveis do projeto (stack, comandos, convenções) viram **proposta de
  CLAUDE.md** no handoff, para todos os agentes se beneficiarem — ele nunca
  edita CLAUDE.md sem autorização explícita.
- **Agentes registrados com linhagem** — sub-subagentes promovidos a
  reutilizáveis entram no inventário (`subagents.md` da memória) e nascem
  com ponteiro para o conhecimento comum do projeto.

## Instalação

### Como plugin (recomendado)

```
/plugin marketplace add pessoaviva/agentesfable5
/plugin install hercules@agentesfable5
```

O plugin instala o agente E os 4 módulos (skills) juntos.

### Uso direto no projeto (sem plugin)

Copie o agente **e os módulos** para o seu projeto:

```
cp agents/hercules.md <seu-projeto>/.claude/agents/
cp -r skills/* <seu-projeto>/.claude/skills/
```

(Neste repositório as cópias já existem em `.claude/agents/` e
`.claude/skills/`; as fontes são `agents/` e `skills/`, e a sincronia é
verificada pelo CI.)

## Uso

```
Crie uma landing page responsiva para uma cafeteria, com seção de menu e contato.
```

```
Use o Hércules para estruturar um site estático com 4 páginas.
```

```
Hércules, guarde que a paleta do projeto é #1B4332 e #D8F3DC.
```

```
Hércules, em modo cirúrgico: corrija o bug do formulário sem tocar em mais nada.
```

```
Hércules, em modo ultra: compare Next.js e Astro para este site e proponha um plano completo antes de implementar.
```

## Estrutura do repositório

```
.claude-plugin/
  plugin.json          # manifesto do plugin
  marketplace.json     # marketplace que distribui o plugin
agents/
  hercules.md          # NÚCLEO do agente (fonte)
skills/
  hercules-planejamento/SKILL.md   # módulos carregados sob demanda (fonte)
  hercules-qualidade/SKILL.md
  hercules-memoria/SKILL.md
  hercules-delegacao/SKILL.md
.claude/
  agents/ · skills/    # cópias para uso direto neste repo (sincronia via CI)
scripts/validate.py    # valida JSONs, frontmatter, sincronia, referências e versão
.github/workflows/validate.yml
CHANGELOG.md · LICENSE
```

## Arquivos que o Hércules mantém nos projetos

```
.claude/agent-memory/hercules/   # memória persistente nativa (MEMORY.md + temáticos)
.hercules/handoffs/              # artefatos efêmeros para outros agentes (gitignored)
DECISIONS.md                     # decisões de custo alto/irreversível (quando houver)
```

E propostas de atualização do `CLAUDE.md` do projeto (só aplicadas pelo
orquestrador/usuário — nunca por conta própria).
