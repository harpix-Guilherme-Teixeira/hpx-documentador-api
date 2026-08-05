# hpx-documentador-api

Plugin do Claude Code com a documentação de API no padrão harpix: acha a
fonte oficial (OpenAPI) por trás do site de documentação, extrai os campos
reais, monta o rascunho, confere campo inventado contra a fonte e publica no
Confluence pelo conector do Atlassian, sempre com aprovação humana antes.

Este repo é um marketplace de plugin. O plugin `doc-api` traz:

- o **MCP `doc-api` embutido** (o pacote npm `hpx-doc-api-mcp`, registrado
  automaticamente na instalação, sem terminal e sem npx na mão);
- a **skill** com os gatilhos de uso, pra conversa normal já cair no método;
- o comando **`/doc-api:documentar`**, porta de entrada única: cole o link da
  documentação da API e siga.

## Instalar

No Claude Code:

```
/plugin marketplace add harpix-Guilherme-Teixeira/hpx-documentador-api
/plugin install doc-api@hpx-documentador-api
```

Reinicie o Claude Code depois de instalar e confirme com `/mcp` que o
servidor `doc-api` aparece conectado. Conecte também o conector do
**Atlassian** (`/mcp`), que é quem publica no Confluence com a sua conta.

**Quem já instalou pelo `npx -y hpx-doc-api-mcp setup`:** o registro antigo
continua funcionando, mas com o plugin ele fica duplicado. Remova com
`claude mcp remove doc-api -s user` e fique só com o do plugin.

## Onde o plugin não chega

No **Claude Desktop** a instalação continua sendo
`npx -y hpx-doc-api-mcp@latest setup`. No **claude.ai pelo navegador e no
celular** a ferramenta ainda não funciona, ela roda como processo local; a
versão por conector remoto está no roadmap.

## Fonte canônica

O método da harpix e as tools moram no pacote npm `hpx-doc-api-mcp`
(repo `hpx-mcp-docapi`). Este plugin é casca: comando e skill apontam pro
método servido pelo próprio MCP (resource `doc-api://metodo/harpix`), então
atualização de método é publicação do pacote npm, não commit aqui. Só mexa
neste repo pra mudar a experiência de instalação e de entrada.
