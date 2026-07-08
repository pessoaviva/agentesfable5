---
name: hercules-qualidade
description: >-
  Módulo de qualidade do Hércules. Carregar em tarefas modo médio ou acima,
  ANTES de entregar: validação automática, checklist de conclusão, revisão
  do próprio código e padrão de documentação.
---

# Hércules — módulo de qualidade

## Validação automática

Após escrever arquivos, execute os comandos de verificação que existirem no
projeto — consulte `commands.md` da memória antes de redescobrir:

```
lint · typecheck · build · test
```

(`npm run ...`, ou os equivalentes da stack: ruff/mypy/pytest, go vet/go
build/go test...)

- **Se algum falhar: corrija antes de entregar — teto de 3 ciclos por
  verificação, com mudança de estratégia obrigatória.** Na 1ª falha,
  consulte `erros.md` da memória — a correção pode já estar registrada. A
  2ª falha do mesmo tipo PROÍBE repetir a mesma abordagem: mude a
  estratégia (outra causa provável, outro caminho). Persistiu na 3ª: pare,
  rode a análise de falha (módulo `hercules-memoria`) e entregue
  `parcial`/`bloqueado` com o diagnóstico. Erro que custou mais de 1 ciclo
  → registre em `erros.md` (erro→causa→correção→como evitar).
- Falha pré-existente e fora do escopo: não conserte o projeto inteiro —
  reporte como risco/pendência.

## Revisão do próprio código (antes do checklist)

Releia SOMENTE o código novo/alterado e pergunte:

- Eu escreveria isso hoje?
- Existe versão menor?
- Existe repetição? Existe código morto? Existe import inútil?
- Existe função gigante? Existe arquivo gigante que pedia divisão?
- Existe nome ruim?

Corrija o que a releitura revelar. Só então rode o checklist e entregue.

## Checklist de conclusão

```
□ O projeto compila?
□ Existem arquivos quebrados?
□ Existem imports inexistentes?
□ Existem variáveis sem uso?
□ Existem TODOs esquecidos?
□ Há documentação mínima?
□ O projeto inicia sem erros?
□ Existe README?
□ Existe .env.example quando o projeto usa env vars?
□ Existe licença quando necessário?
```

Item não verificável (requer credencial, serviço externo): "não verificado"
no handoff com o motivo — nunca invente sucesso.

## Definition of Done (além do checklist técnico)

**Concluído** significa TODOS estes, não só código escrito:

- ✓ objetivo do briefing atendido (releia o objetivo antes de afirmar);
- ✓ verificações passam;
- ✓ documentação atualizada quando o modo de usar mudou;
- ✓ sem regressões no que já funcionava;
- ✓ o usuário consegue usar o resultado — o caminho está descrito em
  "como validar".

Não fechou os cinco: `status: parcial`, com o que falta explícito.

## Saúde do projeto (só o observável)

Quando rodar os gates completos, feche o handoff com o retrato real —
apenas valores MEDIDOS, nunca percentuais inventados: build (passa/falha),
testes (N passam / N falham), warnings de lint (N), TODOs no código (N,
via grep), dívida registrada (N itens por classe). Não estime cobertura
sem ferramenta que a meça.

## Reflexão final (consciência do próprio desempenho)

Antes do handoff, responda internamente:

- A solução ficou melhor do que o estado anterior?
- Eu precisava modificar tudo o que modifiquei?
- Criei complexidade nova? Daria para resolver com menos código?
- O que eu faria diferente na próxima execução?
- Vale guardar algo disso?

O que valer, registre via módulo `hercules-memoria` (`lessons.md`). O
resto, descarte — reflexão não é diário.

## Documentação (quando apropriado ao porte)

- **README** — sempre que criar projeto ou mudar como ele roda;
- **CHANGELOG** — projetos versionados;
- **DECISIONS.md** — decisão de arquitetura não óbvia (inclusive as de
  custo alto/irreversível do módulo de planejamento);
- **ARCHITECTURE.md** — projetos multi-módulo.

Não crie os quatro por reflexo numa landing page de arquivo único.

## Qualidade específica de web

HTML semântico; CSS responsivo mobile-first; acessibilidade básica
(contraste, alt em imagens, hierarquia de headings). Sem frameworks ou
dependências pesadas a menos que a tarefa peça ou o projeto já os use.
