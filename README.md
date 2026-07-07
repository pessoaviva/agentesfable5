# Hércules 🏛️

**Hércules** é um subagente do Claude Code especializado em **criação de
projetos** — sites, landing pages, aplicações web, APIs e scaffolding. Ele não
é um assistente autônomo independente: é invocado pelo Claude (orquestrador)
para executar uma tarefa delimitada, com contexto próprio, e devolve o
resultado num bloco de handoff estruturado.

Este repositório é ao mesmo tempo o **plugin** e o **marketplace** que o
distribui.

## O que ele faz

- **Modos de raciocínio** — declara `Modo: baixo|médio|alto|ultra — motivo`
  em 1 linha antes de agir. Baixo: tarefa mecânica de 1 passo. Médio: 2-4
  passos dependentes (teto padrão). Alto: só para domínios críticos
  (arquitetura, migração, refatoração massiva, banco de dados, segurança,
  escalabilidade, monorepo, mudança de framework, sistema distribuído) ou
  pedido explícito. **Ultra**: só quando solicitado explicitamente — pesquisa
  profunda, comparação de arquiteturas, benchmarks, RFCs, documentação
  oficial e plano completo antes de implementar.
- **Inteligência fixada no Fable 5** — `model: fable`: o Hércules roda
  sempre no Claude Fable 5, independentemente do modelo da sessão principal.
  Exemplo: sessão em Opus 4.8 → o Hércules continua operando com a
  inteligência do Fable 5. Para travar uma versão exata, troque para o ID
  completo (`model: claude-fable-5`). Requisitos: a conta precisa ter acesso
  ao Fable 5 — se o modelo estiver bloqueado pela allowlist da organização
  (`availableModels`) ou pela variável `CLAUDE_CODE_SUBAGENT_MODEL`, o
  Claude Code ignora o valor e cai no modelo herdado da sessão.
- **Planejamento interno obrigatório** — antes de editar qualquer arquivo:
  entende o projeto, detecta a arquitetura existente (framework, linguagem,
  padrão arquitetural, package manager, SO, convenções), classifica o tipo de
  projeto (landing page, SaaS, API, dashboard, CMS, biblioteca, CLI,
  fullstack, mobile, monorepo), lista dependências, identifica riscos e cria
  um plano resumido. **Nunca impõe arquitetura nova onde já existe uma**
  (nada de misturar Vite com Next, Express com Fastify).
- **Quality gates** — antes de finalizar, roda automaticamente
  `lint`/`typecheck`/`build`/`test` (os que existirem no projeto) e corrige
  falhas antes de entregar; valida checklist de conclusão (compila? inicia
  sem erros? imports quebrados? TODOs esquecidos? README? `.env.example`?
  licença?); gera README/CHANGELOG/DECISIONS.md/ARCHITECTURE.md quando
  apropriado ao porte do projeto.
- **Economia de créditos e gestão de contexto** — baixo/médio por padrão,
  leitura seletiva, chamadas agrupadas, resultado compacto. Em projetos
  grandes: resume módulos antigos, nunca relê arquivos já resumidos e mantém
  um mapa interno do projeto.
- **Cache de conhecimento** — persiste o que aprendeu em `.hercules/cache/`
  (`frameworks.md`, `commands.md`, `dependencies.md`, `architecture.md`) para
  não redescobrir a stack a cada invocação.
- **Memória estruturada** — quando pedem para guardar algo, grava em
  `.hercules/memory/` no arquivo adequado (`architecture.md`,
  `preferences.md`, `todos.md`, `bugs.md`, `history.md`, `api.md`) e confirma
  no handoff. Nunca grava segredos.
- **Sistema de prioridades** — em conflito: 1) não quebrar código existente,
  2) manter padrões do projeto, 3) código simples, 4) performance,
  5) features novas, 6) refatorações.
- **Segurança** — nunca expõe secrets, nunca grava API keys, não altera
  `.env` sem autorização, não faz commit automático, não executa scripts
  desconhecidos nem instala dependências suspeitas.
- **Rollback** — antes de editar arquivos existentes, registra em
  `.hercules/memory/history.md` o que mudou, por quê e como desfazer.
- **Delegação recursiva inteligente** — antes de criar sub-subagentes avalia
  tempo estimado, dependências, paralelismo e complexidade; delega só com
  ganho real, senão executa sozinho. Ao final, decide explicitamente:
  **descartar** o sub-subagente ou **registrá-lo** como arquivo reutilizável
  em `.claude/agents/<name>.md` — nunca promoção automática.
- **Comunicação entre agentes** — todo retorno termina com o bloco
  `[HÉRCULES→ORQUESTRADOR]` (handoff completo + métricas); coordenação com
  outros agentes sem canal direto passa por arquivos em
  `.hercules/handoffs/`.

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
[`.claude/agents/hercules.md`](.claude/agents/hercules.md)).

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
  plugin.json        # manifesto do plugin
  marketplace.json   # marketplace que distribui o plugin
agents/
  hercules.md        # definição do subagente (fonte)
.claude/agents/
  hercules.md        # cópia para uso direto neste repositório
```

## Arquivos que o Hércules mantém nos projetos

```
.hercules/
  cache/             # conhecimento do projeto (stack, comandos, mapa)
  memory/            # memória sob demanda (preferências, todos, bugs, histórico...)
  handoffs/          # mensagens para outros agentes
```

## Formato do handoff

Toda invocação termina com:

```
[HÉRCULES→ORQUESTRADOR]

## Handoff
- modo, status, objetivo
- arquivos alterados / criados / removidos
- decisões tomadas, trade-offs, riscos
- pendências, testes executados, como validar, próximos passos
- subagentes (descartados ou registrados), memória/cache

## Métricas
- tempo estimado, arquivos lidos/escritos, chamadas de ferramentas,
  subagentes usados, tokens economizados, complexidade
```
