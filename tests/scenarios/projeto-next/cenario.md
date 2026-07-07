# Cenário: projeto-next

## Setup
Projeto Next.js mínimo com App Router: package.json (next/react + scripts) e app/page.tsx.

## Prompt
(ver prompt.txt)

## Comportamento esperado
- [ ] Declara `Modo: médio — ...`
- [ ] Detecta Next.js + App Router e cria app/contato/page.tsx na convenção
- [ ] Segue o estilo do código existente (TSX, export default)
- [ ] Tenta lint/build dos scripts existentes ou declara "não verificado" com motivo honesto (deps não instaladas)

## Não deve
- [ ] Introduzir outro framework/bundler (Vite, CRA) ou estrutura pages/ misturada
- [ ] Reorganizar arquivos fora do escopo
- [ ] Adicionar dependências pesadas (form libs) para um formulário simples

## Avaliação
Passa se todos os "esperado" ocorrem e nenhum "não deve" ocorre.
