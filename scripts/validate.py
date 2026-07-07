#!/usr/bin/env python3
"""Valida a integridade do plugin Hércules.

Verifica: JSONs do plugin, frontmatter do agente e dos módulos (skills),
sincronia entre as fontes (agents/, skills/) e as cópias de uso direto
(.claude/agents/, .claude/skills/), e consistência da versão com o
CHANGELOG.
"""
import filecmp
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENT_SOURCE = ROOT / "agents" / "hercules.md"
AGENT_COPY = ROOT / ".claude" / "agents" / "hercules.md"
SKILLS = [
    "hercules-planejamento",
    "hercules-qualidade",
    "hercules-memoria",
    "hercules-delegacao",
]
REQUIRED_AGENT_FIELDS = ("name:", "description:", "tools:", "model:")

errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def frontmatter_of(path):
    match = re.match(r"^---\n(.*?)\n---\n", path.read_text(), re.DOTALL)
    check(match, f"{path.relative_to(ROOT)} sem frontmatter YAML")
    return match.group(1) if match else ""


def check_synced(source, copy):
    check(copy.exists(), f"{copy.relative_to(ROOT)} não existe")
    if copy.exists():
        check(filecmp.cmp(source, copy, shallow=False),
              f"{copy.relative_to(ROOT)} divergiu de "
              f"{source.relative_to(ROOT)} — rode: "
              f"cp {source.relative_to(ROOT)} {copy.relative_to(ROOT)}")


plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
check("name" in plugin, "plugin.json sem campo 'name'")
check("version" in plugin, "plugin.json sem campo 'version'")

marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
check(marketplace.get("plugins"), "marketplace.json sem lista 'plugins'")
names = [p.get("name") for p in marketplace.get("plugins", [])]
check(plugin.get("name") in names,
      f"plugin '{plugin.get('name')}' não listado no marketplace.json")

agent_fm = frontmatter_of(AGENT_SOURCE)
for field in REQUIRED_AGENT_FIELDS:
    check(field in agent_fm, f"frontmatter do agente sem campo '{field}'")
check("model: fable" in agent_fm,
      "model deve ser 'fable' (inteligência fixada no Fable 5)")
check("Skill" in agent_fm,
      "agente sem a ferramenta Skill (necessária para carregar os módulos)")
check_synced(AGENT_SOURCE, AGENT_COPY)

for skill in SKILLS:
    source = ROOT / "skills" / skill / "SKILL.md"
    check(source.exists(), f"módulo skills/{skill}/SKILL.md ausente")
    if not source.exists():
        continue
    skill_fm = frontmatter_of(source)
    check(f"name: {skill}" in skill_fm,
          f"módulo {skill}: frontmatter sem 'name: {skill}'")
    check("description:" in skill_fm,
          f"módulo {skill}: frontmatter sem 'description'")
    check_synced(source, ROOT / ".claude" / "skills" / skill / "SKILL.md")
    check(f"`{skill}`" in AGENT_SOURCE.read_text(),
          f"núcleo do agente não referencia o módulo {skill}")

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
