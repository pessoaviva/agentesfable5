#!/usr/bin/env python3
"""Valida a integridade do plugin Hércules.

Verifica: JSONs do plugin, frontmatter do agente, sincronia entre a fonte
(agents/hercules.md) e a cópia de uso direto (.claude/agents/hercules.md),
e consistência da versão com o CHANGELOG.
"""
import filecmp
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "agents" / "hercules.md"
COPY = ROOT / ".claude" / "agents" / "hercules.md"
REQUIRED_FRONTMATTER = ("name:", "description:", "tools:", "model:")

errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
check("name" in plugin, "plugin.json sem campo 'name'")
check("version" in plugin, "plugin.json sem campo 'version'")

marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
check(marketplace.get("plugins"), "marketplace.json sem lista 'plugins'")
names = [p.get("name") for p in marketplace.get("plugins", [])]
check(plugin.get("name") in names,
      f"plugin '{plugin.get('name')}' não listado no marketplace.json")

text = SOURCE.read_text()
match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
check(match, "agents/hercules.md sem frontmatter YAML")
if match:
    frontmatter = match.group(1)
    for field in REQUIRED_FRONTMATTER:
        check(field in frontmatter, f"frontmatter sem campo obrigatório '{field}'")
    check("model: fable" in frontmatter,
          "model deve ser 'fable' (inteligência fixada no Fable 5)")

check(COPY.exists(), ".claude/agents/hercules.md não existe")
if COPY.exists():
    check(filecmp.cmp(SOURCE, COPY, shallow=False),
          ".claude/agents/hercules.md divergiu de agents/hercules.md — "
          "rode: cp agents/hercules.md .claude/agents/hercules.md")

changelog = (ROOT / "CHANGELOG.md").read_text()
check(f"## {plugin.get('version')}" in changelog,
      f"versão {plugin.get('version')} do plugin.json ausente no CHANGELOG.md")

check((ROOT / "LICENSE").exists(), "LICENSE ausente")
check((ROOT / "README.md").exists(), "README.md ausente")

if errors:
    for error in errors:
        print(f"ERRO: {error}")
    sys.exit(1)
print("OK: plugin válido")
