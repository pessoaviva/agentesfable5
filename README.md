# Hércules 🏛️

**Hércules** é um subagente do Claude Code especializado em **criação de
projetos** — sites, landing pages, aplicações web, APIs e scaffolding. Ele não
é um assistente autônomo independente: é invocado pelo Claude (orquestrador)
para executar uma tarefa delimitada, com contexto próprio, e devolve o
resultado num bloco de handoff estruturado. Ele não conversa com o usuário no
meio da execução — dúvidas que só o usuário resolve voltam como
`status: bloqueado` no handoff.

Este repositório é ao mesmo tempo o **plugin** e o **marketplace** que o
distribui.

## O que ele faz

- **Modos de raciocínio proporcionais** — declara
  `Modo: baixo|médio|alto|ultra — motivo` em 1 linha antes de agir, e o rito
  inteiro escala com o modo: em modo baixo, protocolo mínimo e handoff curto
  de 4 linhas; em médio+, plano prévio, checklist completo e handoff rico.
  Alto: só para domínios críticos (arquitetura, migração, refatoração
  massiva, banco de dados, segurança, escalabilidade, monorepo, mudança de
  framework, sistema distribuído) ou pedido explícito. **Ultra**: só quando
  solicitado explicitamente — pesquisa profunda, comparação de arquiteturas,
  benchmarks, RFCs e plano completo antes de implementar.
  *Nota honesta: os modos controlam o processo (exploração, plano,
  validação, verbosidade), não o esforço de raciocínio do modelo — esse é
  herdado da sessão.*
- **Inteligência fixada no Fable 5** — `model: fable`: o Hércules roda
  sempre no Claude Fable 5, independentemente do modelo da sessão principal.
  Exemplo: sessão em Opus 4.8 → o Hércules continua operando com a
  inteligência do Fable 5. Para travar uma versão exata, troque para o ID
  completo (`model: claude-fable-5`). Requisitos: a conta precisa ter acesso
  ao Fable 5 — se o modelo estiver bloqueado pela allowlist da organização
  (`availableModels`) ou pela variável `CLAUDE_CODE_SUBAGENT_MODEL`, o
  Claude Code ignora o valor e cai no modelo herdado da sessão.
- **Planejamento interno obrigatório** (modo médio+) — antes de editar
  qualquer arquivo: entende o projeto, detecta a arquitetura existente
  (framework, linguagem, padrão arquitetural, package manager, convenções),
  classifica o tipo de projeto (landing page, SaaS, API, dashboard, CMS,
  biblioteca, CLI, fullstack, mobile, monorepo), lista dependências,
  identifica riscos e escreve um plano resumido. **Nunca impõe arquitetura
  nova onde já existe uma** (nada de misturar Vite com Next, Express com
  Fastify).
- **Quality gates com teto de gasto** — roda `lint`/`typecheck`/`build`/
  `test` (os que existirem) e corrige falhas antes de entregar, com **máximo
  de 3 ciclos de correção por verificação** — depois disso para e reporta
  parcial/bloqueado com diagnóstico, em vez de queimar créditos em loop.
  Checklist de conclusão (compila? inicia sem erros? imports quebrados?
  TODOs? README? `.env.example`? licença?) proporcional ao modo. `maxTurns`
  limita o orçamento total da invocação.
- **Memória persistente nativa** — usa o campo `memory: project` da
  plataforma: o diretório `.claude/agent-memory/hercules/` sobrevive entre
  invocações e o índice `MEMORY.md` é **injetado automaticamente** no
  contexto (consultar não custa chamadas). Arquivos temáticos: `stack.md`,
  `commands.md`, `architecture.md`, `preferences.md`, `todos.md`, `bugs.md`,
  `api.md`, `history.md`. Pedidos de "guarde X" vão para o arquivo adequado
  com confirmação no handoff. Nunca grava segredos. Formatos legados
  (`.hercules/memory*`, `.hercules/cache/`) são migrados automaticamente.
- **Economia de créditos e gestão de contexto** — leitura seletiva, chamadas
  agrupadas, resultado compacto; em projetos grandes resume módulos antigos,
  nunca relê o já resumido e mantém o mapa do projeto na memória.
- **Sistema de prioridades** — em conflito: 1) não quebrar código existente,
  2) manter padrões do projeto, 3) código simples, 4) performance,
  5) features novas, 6) refatorações.
- **Segurança** — nunca expõe secrets, nunca grava API keys, não altera
  `.env` sem autorização, não faz commit automático, não executa scripts
  desconhecidos nem instala dependências suspeitas. *Essas regras são
  comportamentais (prompt); para garantia mecânica, adicione deny rules nas
  [permissions](https://code.claude.com/docs/en/permissions) da sua sessão —
  ex.: `Bash(git commit*)` em `permissions.deny`.*
- **Rollback via git** — em repositório git com working tree limpo, o git é
  o rollback e o handoff informa como reverter; fora de git (ou com
  alterações não commitadas nos arquivos alvo), registra o conteúdo original
  em `history.md` antes de sobrescrever.
- **Delegação recursiva inteligente** — avalia tempo, dependências,
  paralelismo e complexidade antes de criar sub-subagentes (ferramenta
  `Agent`; requer Claude Code v2.1.172+); delega só com ganho real. Ao
  final, decide explicitamente: **descartar** ou **registrar** o
  sub-subagente como arquivo reutilizável em `.claude/agents/<name>.md` —
  nunca promoção automática.
- **Comunicação entre agentes** — todo retorno termina com o bloco
  `[HÉRCULES→ORQUESTRADOR]`; coordenação com outros agentes sem canal direto
  passa por `.hercules/handoffs/` (efêmero, vai para o `.gitignore`).
- **Métricas honestas** — o handoff completo fecha com métricas apenas do
  observável (arquivos lidos/escritos, comandos executados, subagentes,
  complexidade) — nada de estimar tokens ou tempo que o modelo não mede.

## Instalação

### Como plugin (recomendado)

No Claude Code:

```
/plugin marketplace add pessoaviva/agentesfable5
/plugin install hercules@agentesfable5
```

### Uso direto no projeto (sem plugin)

Copie [`agents/hercules.md`](agents/hercules.md) para `.claude/agents/` do seu
projeto (neste repositório a cópia já existe em
[`.claude/agents/hercules.md`](.claude/agents/hercules.md); a fonte é
`agents/hercules.md` e a sincronia é verificada pelo CI).

## Uso

Peça naturalmente — o orquestrador invoca o Hércules quando a tarefa é criar
ou desenvolver um projeto:

```
Crie uma landing page responsiva para uma cafeteria, com seção de menu e contato.
```

Ou invoque explicitamente:

```
Use o Hércules para estruturar um site estático com 4 páginas.
```

Para usar a memória:

```
Hércules, guarde que a paleta do projeto é #1B4332 e #D8F3DC.
```

Para o modo Ultra (só roda se pedido explicitamente):

```
Hércules, em modo ultra: compare Next.js e Astro para este site e proponha um plano completo antes de implementar.
```

## Estrutura do repositório

```
.claude-plugin/
  plugin.json          # manifesto do plugin
  marketplace.json     # marketplace que distribui o plugin
agents/
  hercules.md          # definição do subagente (FONTE)
.claude/agents/
  hercules.md          # cópia para uso direto neste repositório (sincronia via CI)
scripts/
  validate.py          # valida JSONs, frontmatter, sincronia e versão
.github/workflows/
  validate.yml         # roda a validação em cada push/PR
CHANGELOG.md · LICENSE
```

## Arquivos que o Hércules mantém nos projetos

```
.claude/agent-memory/hercules/   # memória persistente (nativa; MEMORY.md + temáticos)
.hercules/handoffs/              # mensagens efêmeras para outros agentes (gitignored)
```

## Formato do handoff

Modo baixo (curto):

```
[HÉRCULES→ORQUESTRADOR]
modo: baixo | status: concluído
resultado: ...
arquivos: ...
verificação: ...
```

Modo médio/alto/ultra (completo): objetivo, arquivos alterados/criados/
removidos, decisões, trade-offs, riscos, pendências, verificação, como
validar, **como reverter**, próximos passos, subagentes, memória — e o bloco
de métricas observáveis.
