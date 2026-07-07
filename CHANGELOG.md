# Changelog

## 1.2.0 — 2026-07-07

Correções da revisão externa do agente:

- **Proporcionalidade por modo**: o rito inteiro (protocolo de início,
  quality gates, handoff) agora escala com o modo; modo baixo usa handoff
  curto e validação mínima, eliminando a burocracia fixa que anulava a
  economia de créditos.
- **Memória nativa**: migração do `.hercules/memory/` artesanal para o campo
  `memory: project` da plataforma (`.claude/agent-memory/hercules/`), com
  `MEMORY.md` injetado automaticamente no contexto e arquivos temáticos
  (stack, commands, architecture, preferences, todos, bugs, api, history).
  O cache `.hercules/cache/` foi absorvido pela memória. Migração automática
  do formato legado.
- **Métricas só observáveis**: removidas "tokens economizados", "chamadas de
  ferramentas" e "tempo estimado" (o modelo não consegue medi-las e
  inventaria números); mantidas arquivos lidos/escritos, comandos
  executados, subagentes e complexidade.
- **Teto de gasto**: `maxTurns: 100` no frontmatter e máximo de 3 ciclos de
  correção por verificação que falha — depois disso o agente para e reporta
  parcial/bloqueado com diagnóstico.
- **Rollback invertido**: em repositório git com working tree limpo, o git é
  o rollback (nenhum registro manual); registro em `history.md` só fora de
  git ou com working tree sujo. Novo campo "como reverter" no handoff.
- **Política de git para `.hercules/`**: restou apenas `handoffs/`
  (efêmero), com instrução de adicionar ao `.gitignore`.
- **`Task` → `Agent`**: nome canônico da ferramenta de delegação no
  frontmatter; documentado o requisito de versão (v2.1.172+) para
  sub-subagentes aninhados.
- **Subagente não pergunta ao usuário**: "na dúvida, pergunte" corrigido
  para "retorne status: bloqueado com a pergunta no handoff".
- **Honestidade documentada**: modos controlam o processo, não o esforço de
  raciocínio do modelo (herdado da sessão); regras de segurança são
  comportamentais — garantia mecânica vem das permissions da sessão.
- **Exemplos calibradores** no system prompt (modo baixo completo e esboço
  de modo médio).
- **Descrição bilíngue** (PT + EN) para robustez do matching do orquestrador.
- **Higiene do repositório**: LICENSE (MIT), este CHANGELOG, script de
  validação (`scripts/validate.py`) e CI (GitHub Actions) verificando JSONs,
  frontmatter, sincronia das cópias e consistência de versão.

## 1.1.0 — 2026-07-07

- 17 melhorias ao system prompt: quality gates, planejamento interno
  obrigatório, detecção de arquitetura, validação automática, gestão de
  janela de contexto, cache de conhecimento, memória estruturada,
  classificação do tipo de projeto, delegação inteligente, sistema de
  prioridades, regras de segurança, rollback, critérios objetivos de modo
  alto, padrão de documentação, handoff rico, modo ultra e métricas.
- Modelo fixado no Claude Fable 5 (`model: fable`) em vez de herdar o da
  sessão.

## 1.0.0 — 2026-07-07

- Versão inicial: subagente Hércules empacotado como plugin do Claude Code
  com marketplace no próprio repositório, modos de raciocínio
  baixo/médio/alto, economia de créditos, delegação recursiva controlada,
  memória sob demanda e handoff estruturado.
