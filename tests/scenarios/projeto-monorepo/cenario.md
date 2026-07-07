# Cenário: projeto-monorepo

## Setup
Monorepo npm workspaces: package.json raiz com workspaces packages/*,
pacotes @app/web e @app/api existentes.

## Prompt
(ver prompt.txt)

## Comportamento esperado
- [ ] Declara `Modo: alto — monorepo` (domínio de modo alto)
- [ ] Define o CONTRATO primeiro (assinatura de formatDate) antes de tocar nos consumidores
- [ ] Cria packages/utils seguindo a convenção dos pacotes existentes (@app/utils, main, estrutura src/)
- [ ] Adiciona a dependência @app/utils nos package.json de web e api (workspace)
- [ ] Valida o conjunto (npm install/execução) ou declara "não verificado" com motivo

## Não deve
- [ ] Duplicar a função em web e api em vez de criar o pacote
- [ ] Quebrar a convenção de nomes/estrutura dos pacotes existentes
- [ ] Tratar como modo baixo/médio sem justificar

## Avaliação
Passa se todos os "esperado" ocorrem e nenhum "não deve" ocorre.
Este cenário mede a regra de modo alto e contratos-antes-de-paralelizar.
