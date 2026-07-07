---
name: hercules-planejamento
description: >-
  Módulo de planejamento do Hércules. Carregar em tarefas modo médio ou
  acima, ANTES de editar qualquer arquivo: protocolo de início, análise de
  impacto, custo de mudança e rollback.
---

# Hércules — módulo de planejamento

## Protocolo de início (antes de editar qualquer arquivo)

1. **Entenda o projeto.** Comece pela memória persistente (já injetada);
   complete com README, manifesto de dependências e estrutura de diretórios
   apenas no que a memória não cobre.
2. **Detecte a arquitetura existente:** framework, linguagem e versão,
   padrão arquitetural, package manager, ambiente de execução, convenções
   (nomes, lint, formatação, estrutura de pastas).
   **NUNCA imponha arquitetura nova onde existir uma estabelecida.** Não
   misture stacks (Vite com Next, Express com Fastify). Em projeto novo,
   escolha a stack mais simples que atende à tarefa.
3. **Classifique o tipo de projeto** e adapte a estratégia: Landing Page ·
   SaaS · API · Dashboard · CMS · Biblioteca · CLI · Fullstack · Mobile ·
   Monorepo.
4. **Liste as dependências** relevantes (existentes e a adicionar).
5. **Identifique riscos** (o que pode quebrar, o que é irreversível) e
   classifique cada um: baixo · médio · alto · crítico.
6. **Escreva o plano resumido** (2-5 linhas em médio; em alto/ultra,
   estruturado por fases: análise → implementação → validação → entrega).
   Só então modifique arquivos.

## Detector de inconsistências

Durante a detecção (passo 2), confira a coerência entre as fontes de
verdade: manifesto × lockfile × tsconfig/configs × versões declaradas × CI.
Exemplo: `package.json` diz React 19, `tsconfig` assume React 18. Achou
divergência? **Não escolha um lado em silêncio**: reporte como risco
(alto) no handoff e, se a tarefa depender da resposta, `bloqueado`.

## Análise de impacto (antes de editar arquivo EXISTENTE)

Liste, com evidência (Grep pelos importadores é barato):

- Quem importa este arquivo? Quem depende dele?
- O que quebra se a interface mudar?
- Existe API pública exposta (exports, endpoints, eventos)?
- Existe contrato combinado (tipos compartilhados, schema, formato de
  resposta — confira `api.md` da memória)?

São **automaticamente custo alto (no mínimo)**, por menores que pareçam:
alterar API pública · renomear endpoint · trocar banco/ORM · migração
destrutiva · remover comportamento em uso · quebrar contrato combinado.
Nenhuma dessas acontece sem a autorização do fluxo abaixo.

## Custo de mudança (classifique antes de implementar)

- **baixo** — local, reversível, sem efeito fora do arquivo.
- **médio** — afeta poucos módulos, reversível com esforço pequeno.
- **alto** — afeta arquitetura, contratos ou muitos módulos.
- **irreversível** — perda de dados, migração destrutiva, remoção de API
  usada.

Se **alto** ou **irreversível**:

1. explique o motivo no plano;
2. registre em `DECISIONS.md` (o que, por quê, alternativas descartadas);
3. confirme com o orquestrador — se a autorização não estiver clara na
   tarefa recebida, retorne `status: bloqueado` com a decisão formulada em
   vez de assumir.

## Rollback

- **Repositório git com working tree limpo nos arquivos alvo: não registre
  nada.** O git é o rollback; informe no handoff como reverter
  (`git checkout -- <arquivos>` ou o commit a reverter).
- **Fora de git, ou working tree sujo nos arquivos alvo:** antes de
  sobrescrever, registre em `history.md` da memória: arquivos, resumo,
  motivo e o conteúdo original dos trechos que vai destruir.
- Nunca delete ou sobrescreva algo irrecuperável sem registro de como
  desfazer.
