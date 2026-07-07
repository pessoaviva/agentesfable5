#!/usr/bin/env bash
# Roda um cenário de avaliação do Hércules em diretório temporário isolado.
# Uso: tests/run.sh <nome-do-cenario>        (ex.: tests/run.sh projeto-next)
# Requer: claude CLI autenticado. Consome créditos — use antes de releases.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CENARIO="${1:?uso: tests/run.sh <nome-do-cenario>}"
DIR="$ROOT/tests/scenarios/$CENARIO"
[ -d "$DIR" ] || { echo "cenário não existe: $CENARIO"; ls "$ROOT/tests/scenarios"; exit 1; }
command -v claude >/dev/null || { echo "claude CLI não encontrado no PATH"; exit 1; }

TMP="$(mktemp -d)"
cp -r "$DIR/fixture/." "$TMP/"
mkdir -p "$TMP/.claude"
cp -r "$ROOT/.claude/agents" "$TMP/.claude/agents"
cp -r "$ROOT/.claude/skills" "$TMP/.claude/skills"
git -C "$TMP" init -q
git -C "$TMP" add -A
git -C "$TMP" -c user.email=eval@local -c user.name=eval commit -qm fixture

echo "== Cenário:  $CENARIO"
echo "== Sandbox:  $TMP"
echo "== Prompt:   $(cat "$DIR/prompt.txt")"
echo "== Critérios: $DIR/cenario.md"
echo "== Executando..."
(cd "$TMP" && claude --agent hercules -p "$(cat "$DIR/prompt.txt")")

echo
echo "== Arquivos alterados no sandbox:"
git -C "$TMP" status --short
echo
echo "Avalie a saída acima contra o checklist de $DIR/cenario.md"
echo "Sandbox preservado em: $TMP (apague quando terminar)"
