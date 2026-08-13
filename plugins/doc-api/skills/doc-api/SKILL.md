---
name: doc-api
description: Documenta a série completa de um conector no Confluence da harpix, 4 modelos encadeados, documentação de API, padrão de domínio de dados no BigQuery, de-para do conector pro domínio e análise de aderência multi plataforma. Use SEMPRE que o usuário disser "doc-api", "documentar a API X", "documentar o endpoint Y", "fazer a doc dessa API no Confluence", "modelar o domínio no BigQuery", "fazer o de-para", "análise de aderência", ou trouxer um link de documentação de API (developer.*, developers.*, swagger, OpenAPI, Redoc, Scalar) com intenção de virar página. A extração e a verificação vêm do MCP doc-api que este plugin registra; o método completo mora no próprio MCP.
---

# doc-api, a série de documentos de conector no padrão harpix

Este plugin registra o MCP `doc-api`, que é quem extrai o schema da fonte
oficial e confere campo inventado. O seu papel é seguir o método da harpix,
que viaja dentro do MCP.

A série completa tem 4 modelos encadeados, e o método detalha os quatro:
documentação de API (a fundação), padrão de domínio de dados no BigQuery,
de-para do conector pro domínio e análise de aderência multi plataforma.
Ao fechar um documento, ofereça o próximo da série.

**Primeiro passo obrigatório: carregue o método.** Leia o resource
`doc-api://metodo/harpix` do MCP `doc-api` (ou invoque o prompt
`doc_api_method`) e siga o que ele diz. Não escreva documentação de API sem
ele carregado, e nunca preencha campo, tipo ou exemplo de memória.

O essencial do fluxo, que o método detalha:

1. `discover_api` no link que a pessoa mandar, acha o OpenAPI por trás do site.
2. `fetch_openapi` com `filtro` + `get_operation` na operação escolhida.
3. `montar_rascunho` monta as tabelas direto do spec, você preenche só o
   julgamento (prosa, regras de negócio, regras de ouro, checklist).
4. `verify_against_source` antes de mostrar qualquer rascunho.
5. PARE para aprovação humana. Só depois publique, pelo conector do Atlassian,
   na página que a pessoa criar e mandar o link. Timeout no publish não
   significa falha: confira o estado real antes de reenviar, retry cego duplica.

Se o MCP `doc-api` não aparecer em `/mcp`, peça pra pessoa reiniciar o Claude
Code. Se pedirem algo que a ferramenta ainda não faz (PDF, dicionário Sankhya,
cruzamento de leiaute), diga que ainda não existe e siga pelo caminho manual.
