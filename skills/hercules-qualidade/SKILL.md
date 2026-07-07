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

- **Se algum falhar: corrija antes de entregar — teto de 3 ciclos de
  correção por verificação.** Na 3ª falha consecutiva da mesma verificação,
  pare e entregue `status: parcial` ou `bloqueado` com o diagnóstico do que
  tentou. Não queime o orçamento em loop.
- Falha pré-existente e fora do escopo: não conserte o projeto inteiro —
  reporte como risco/pendência.

## Revisão do próprio código (antes do checklist)

Releia SOMENTE o código novo/alterado e pergunte:

- Eu escreveria isso hoje?
- Existe versão menor?
- Existe repetição?
- Existe código morto?
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
