# Changelog

## 2.0.0 — 2026-07-07

Motor de execução e melhoria contínua — o agente passa a avaliar as
próprias decisões ao longo do tempo, não só seguir regras.

Adicionado:

- **Ciclo de execução** no núcleo: objetivo → planejamento → execução →
  validação → auto-revisão → aprendizado → handoff; em alto/ultra o plano é
  estruturado por fases; em médio+ as fases são espelhadas no TodoWrite
  (estado visível — versão leve da state machine proposta).
- **Validação do objetivo** antes de gastar contexto: claro? suficiente?
  conflito? dependência externa? risco? — reprova → bloqueado imediato.
- **Definition of Done**: concluído = objetivo atendido + verificações
  passam + docs atualizadas + sem regressões + usuário consegue usar.
- **Autocorreção com mudança de estratégia**: a 2ª falha do mesmo tipo
  proíbe repetir a abordagem; a 3ª dispara análise de falha e entrega
  parcial/bloqueada (antes: apenas parava).
- **Análise de falha**: causa classificada (contexto, externo, bug próprio,
  dependência, instrução, ferramenta) e registrada em lessons.md.
- **Reflexão final (consciência do próprio desempenho)**: ficou melhor?
  precisava tocar tudo isso? criei complexidade? menos código resolveria?
  o que faria diferente? — o durável vai para lessons.md.
- **Aprendizado que muda estratégia**: lessons.md estruturado
  (funcionou | falhou | da próxima vez) e consultado antes de tarefa
  parecida — adaptar abordagem, não acumular anotações.
- **Padrões recorrentes**: sequências repetidas do projeto (ex.: controller
  → service → repository → DTO) registradas em architecture.md e seguidas.
- **Detector de inconsistências**: coerência manifesto × lockfile × configs
  × CI verificada no planejamento; divergência → risco alto, nunca escolha
  silenciosa de um lado.
- **Restrições automáticas de custo alto**: alterar API pública, renomear
  endpoint, trocar banco/ORM, migração destrutiva, remover comportamento em
  uso — sempre exigem o fluxo de autorização.
- **Prioridade de achados (P0)**: problema que impede a tarefa atual é
  corrigido; o resto é registrado classificado, sem desviar do plano.
- **Riscos classificados** (baixo/médio/alto/crítico) no plano e no handoff,
  somados ao rótulo de confiança.
- **Saúde do projeto observável**: retrato só de valores medidos (build,
  testes N/N, warnings N, TODOs N, dívida N por classe).
- **Otimização ampliada** na auto-revisão: imports inúteis, funções e
  arquivos gigantes.
- **Perfil do projeto**: stack.md passa a cobrir deploy/ambiente/contexto.
- **Convenção de módulos de stack** (`hercules-stack-<nome>`): skills
  opcionais por tecnologia, carregadas junto com o planejamento quando a
  stack detectada tiver uma.

Rejeitado por decisão de design (registrado para não voltar):

- Knowledge graph de tecnologias — o modelo já conhece as relações
  (Next→React→TS); manter grafo em arquivo é burocracia que viola "menos
  arquivos".
- Percentuais de saúde/cobertura e benchmark com tempo gasto e taxa de
  sucesso — o agente não mede tempo nem cobertura sem ferramenta; números
  inventados violam o sistema de confiança (v1.2.0).
- Scores numéricos de especialização dinâmica — mesma razão; a fronteira de
  especialidade declarada + delegação já resolve.
- State machine formal de 9 estados — subagente não é processo
  longa-duração; fases no TodoWrite entregam o valor sem o aparato.
- Pacotes de stack pré-fabricados — a convenção foi criada, mas conteúdo
  genérico que o modelo já sabe não será embarcado.

## 1.4.0 — 2026-07-07

Trabalho em equipe: orquestrador, agentes simultâneos e sub-subagentes.

- **Briefing de entrada**: a description agora ensina o orquestrador a
  invocar (objetivo, escopo, restrições, decisões, paralelismo); nova seção
  no núcleo define o comportamento com briefing incompleto (lacuna barata →
  assume e declara; lacuna estrutural → bloqueado).
- **Checkpoint de retomada**: handoffs `parcial`/`bloqueado` incluem bloco
  Retomada (pronto/falta/preciso de/contexto mínimo) para retomada via
  SendMessage ou reinvocação barata.
- **Segurança de concorrência**: nova seção "Trabalho em paralelo" no
  núcleo — snapshot do estado dos arquivos em escopo no início, reconferência
  antes de entregar, e parada obrigatória ao detectar mudança externa;
  recomendação de isolation: worktree para agentes paralelos.
- **Orquestrador como roteador**: comunicação entre agentes passa pelo
  handoff (novo campo `mensagem-para`); `.hercules/handoffs/` rebaixado a
  canal de artefatos grandes, com formato de mensagem e ciclo de vida
  definidos.
- **Delegação que se encaixa**: contratos compartilhados fixados ANTES de
  paralelizar (tokens, interfaces, rotas, como dados imutáveis), escopos
  disjuntos, handoff curto exigido dos sub-subagentes, integração final
  (validação sobre o todo) como responsabilidade do Hércules, e alerta de
  travamento por prompt de permissão em background.
- **Conhecimento compartilhado**: distinção privado × compartilhado no
  módulo de memória; fatos duráveis do projeto viram proposta de CLAUDE.md
  (novo campo `proposta CLAUDE.md` no handoff); edição direta do CLAUDE.md
  só com autorização explícita.
- **Inventário de subagentes**: novo `subagents.md` na memória; agentes
  registrados nascem com ponteiro para o conhecimento comum do projeto e
  handoff curto no template.
- **TodoWrite com propósito**: em tarefas médio+, a lista de tarefas é o
  canal de progresso ao vivo (o agente roda em background).

## 1.3.0 — 2026-07-07

Rearquitetura do agente: núcleo mínimo + módulos sob demanda.

- **Modularização**: o prompt monolítico (356 linhas) virou um núcleo de
  ~210 linhas (missão, modos, decisão, confiança, prioridades, segurança,
  economia, memória, handoff) + 4 módulos carregados sob demanda via skill:
  `hercules-planejamento`, `hercules-qualidade`, `hercules-memoria`,
  `hercules-delegacao`. Modo baixo roda só com o núcleo. Ferramenta `Skill`
  adicionada ao agente; fallback definido quando um módulo não está
  disponível.
- **Missão**: o agente agora é definido pelo objetivo (projetos manteníveis
  por outro desenvolvedor meses depois), não só pelo que faz.
- **Sistema de confiança (anti-alucinação)**: afirmações rotuladas como
  comprovado/validado/inferido/hipótese/suposição; hipótese nunca é
  apresentada como fato; riscos do handoff carregam o rótulo.
- **Núcleo de decisão**: perguntas obrigatórias antes de criar qualquer
  estrutura, incluindo o detector de overengineering ("precisa existir — ou
  pode ser uma função?"), heurísticas de minimalismo (menos arquivos,
  dependências, abstrações, estados, configuração, código), princípio de
  estabilidade (previsível > brilhante; 2 soluções → a mais simples; 3 → a
  mais conhecida) e limite de criatividade (nunca inventar arquitetura,
  padrões ou convenções).
- **Custo de mudança**: classificação baixo/médio/alto/irreversível;
  alto/irreversível exige justificativa, registro em DECISIONS.md e
  confirmação do orquestrador.
- **Análise de impacto**: antes de editar arquivo existente — quem importa,
  quem depende, o que quebra, API pública, contratos.
- **Aprendizado interno**: pós-tarefa médio+, o agente registra em
  lessons.md o que funcionou/falhou/não repetir.
- **Dívida técnica**: nunca corrigida de passagem — registrada em todos.md
  com classificação baixa/média/alta/crítica.
- **Novos modificadores de modo**: **cirúrgico** (modifica somente o
  necessário; sem reorganizar/reformatar/mover) e **legacy** (projetos
  antigos; compatibilidade acima de tudo), combináveis com qualquer modo.
- **Revisão do próprio código**: antes de entregar, releitura apenas do
  código novo (versão menor? repetição? código morto? nome ruim?).
- **Especialização declarada**: forte em scaffolding/web/frontend/backend/
  APIs/landing pages; ML, infra, segurança ofensiva, compiladores, kernel,
  renderização e blockchain são delegados ou devolvidos ao orquestrador.
- Validador e CI atualizados: verificam os módulos (frontmatter, sincronia
  das cópias em .claude/skills/ e referências no núcleo).

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
