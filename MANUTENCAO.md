# Manutenção do Hércules

## Revisão anti prompt-drift (obrigatória antes de cada versão minor)

Prompt cresce como código: acumula regra morta, duplicada e conflitante —
e quanto maior, menor a aderência do modelo. Para CADA regra do núcleo e
dos módulos, pergunte:

1. Essa regra ainda faz sentido?
2. Existe outra regra igual ou quase igual? (duplicação → funde)
3. Ela conflita com a Constituição ou com outra regra? (a Constituição
   decide; ajuste ou remova a perdedora)
4. Pode ser removida, encurtada ou movida do núcleo para um módulo?

Remoção de regra é decisão de design: registre no CHANGELOG.

## Orçamento de tamanho

- Núcleo (`agents/hercules.md`): ≤ ~320 linhas. Estourou → mover para
  módulo ou cortar.
- Módulo (`skills/*/SKILL.md`): ≤ ~120 linhas. Estourou → dividir ou cortar.
- Regra nova só entra se cobrir algo que NENHUMA regra existente cobre.

## Checklist de release

1. `python3 scripts/validate.py` verde.
2. Revisão anti-drift feita (acima).
3. Rodar ao menos 2 cenários de `tests/` — 1 feliz (vazio/next/fastapi) e
   1 adversarial (quebrado/legado) — e avaliar contra os checklists.
4. CHANGELOG atualizado; versão em `.claude-plugin/plugin.json`.
5. Cópias sincronizadas (`cp agents/... skills/... → .claude/`).
6. Commit + push; CI verde.
