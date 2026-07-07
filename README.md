# Hércules 🏛️

**Hércules** é um subagente do Claude Code especializado em **criação de
projetos** — sites, landing pages, aplicações web, APIs e scaffolding. Ele não
é um assistente autônomo independente: é invocado pelo Claude (orquestrador)
para executar uma tarefa delimitada, com contexto próprio, e devolve o
resultado num bloco de handoff estruturado.

Este repositório é ao mesmo tempo o **plugin** e o **marketplace** que o
distribui.

## O que ele faz

- **Modos de raciocínio** — declara `Modo: baixo|médio|alto — motivo` em 1
  linha antes de agir. Baixo: tarefa mecânica de 1 passo. Médio: 2-4 passos
  dependentes (teto padrão). Alto: só com pedido explícito ou ambiguidade
  real (trade-offs, decisão irreversível, hipóteses concorrentes).
- **Economia de créditos** — baixo/médio por padrão, leitura seletiva,
  chamadas agrupadas, resultado compacto. Proibido criar sub-subagente para
  tarefa de 1 chamada.
- **Inteligência herdada** — `model: inherit`: roda com o mesmo modelo da
  sessão principal. Se a sessão usa Claude Fable 5, o Hércules opera com a
  inteligência do Fable 5.
- **Delegação recursiva controlada** — pode criar sub-subagentes apenas para
  unidades independentes/paralelizáveis ou especialidade que ele não tem. Ao
  final, decide explicitamente: **descartar** o sub-subagente ou
  **registrá-lo** como arquivo reutilizável em `.claude/agents/<name>.md`
  (com `name`, `description` e `tools` mínimos) — nunca promoção automática.
- **Memória sob demanda** — quando pedem para guardar algo, grava em
  `.hercules/memory.md` no projeto e confirma no handoff. Nunca grava
  segredos.
- **Comunicação entre agentes** — todo retorno termina com o bloco
  `[HÉRCULES→ORQUESTRADOR]` (modo, status, artefatos, verificação,
  pendências); coordenação com outros agentes sem canal direto passa por
  arquivos em `.hercules/handoffs/`.

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

## Formato do handoff

Toda invocação termina com:

```
[HÉRCULES→ORQUESTRADOR]
modo: ...
status: concluído | parcial | bloqueado
resultado: ...
artefatos: ...
verificação: ...
subagentes: ...
memória: ...
pendências: ...
```
