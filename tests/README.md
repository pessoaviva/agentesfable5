# Testes do Hércules — suíte de cenários

Desenvolver o agente é engenharia de software, não edição de prompt: cada
mudança no núcleo ou nos módulos pode regredir um comportamento. Esta suíte
define 7 cenários com fixtures reais e critérios objetivos de avaliação.

| Cenário | O que mede |
|---|---|
| `projeto-vazio` | escolha de stack mínima, qualidade web, docs proporcionais |
| `projeto-next` | detecção de arquitetura, respeito a convenções |
| `projeto-laravel` | detecção fora do ecossistema JS |
| `projeto-fastapi` | ECONOMIA: modo baixo, handoff curto, zero burocracia |
| `projeto-quebrado` | escopo (não consertar o mundo) e honestidade de verificação |
| `projeto-legado` | contenção: modificador legacy, zero modernização não pedida |
| `projeto-monorepo` | regra de modo alto, contratos antes de tocar consumidores |

## Estrutura

Cada cenário: `cenario.md` (setup + checklist esperado/não-deve),
`prompt.txt` (a tarefa) e `fixture/` (o projeto de teste).

## Como rodar

```
tests/run.sh projeto-next
```

O runner copia o fixture para um sandbox temporário com git iniciado,
instala o agente e os módulos (`.claude/`), executa
`claude --agent hercules -p "<prompt>"` e mostra o diff. A avaliação é
feita contra o checklist do `cenario.md` — por humano ou por LLM-juiz
(cole a saída + o cenario.md e pergunte "passa?").

## O que roda no CI

Só a validação estrutural (`scripts/validate.py`): os cenários existem e
estão completos. A execução comportamental consome créditos de API — rode
localmente pelo menos 2 cenários (1 feliz + 1 adversarial: quebrado ou
legado) antes de cada release, conforme MANUTENCAO.md.
