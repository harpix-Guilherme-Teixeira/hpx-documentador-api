---
description: Documenta uma API no padrao harpix, da fonte oficial ate a pagina no Confluence
argument-hint: "[link do site de documentacao da API, opcional]"
---

Você vai documentar uma API no padrão da harpix usando o MCP `doc-api`.

1. Carregue o método: leia o resource `doc-api://metodo/harpix` do MCP `doc-api`
   (ou invoque o prompt `doc_api_method`). Ele traz o fluxo completo, a estrutura
   de seção obrigatória e as regras de prosa. Siga ele à risca, ele é a fonte da
   verdade deste trabalho, não este comando.
2. Se veio um link em `$ARGUMENTS`, não pergunte nada: rode `discover_api` nele
   imediatamente e confirme com a pessoa o que foi encontrado.
3. Se não veio link, abra a conversa como o método manda: fluxo em duas linhas e
   uma única pergunta, o link do site de documentação da API.

Se o MCP `doc-api` não estiver conectado, diga à pessoa que o plugin precisa de
uma reinicialização do Claude Code após a instalação, e que dá pra conferir com
`/mcp`. Não tente documentar de memória, nunca.
