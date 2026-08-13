---
name: doc-api
description: Documenta a série completa de um conector no Confluence da harpix, extraindo campo, tipo e obrigatoriedade da fonte oficial por script, nunca de memória. A série tem 4 modelos encadeados, documentação de API, padrão de domínio de dados no BigQuery, de-para do conector pro domínio e análise de aderência multi plataforma. Use SEMPRE que o usuário disser "doc-api", "documentar a API X", "documentar o endpoint Y", "fazer a doc dessa API", "atualizar a doc da API", "cruzar a API com o leiaute", "modelar o domínio no BigQuery", "fazer o de-para", "análise de aderência", ou trouxer um link de documentação de API (developer.*, developers.*, swagger, OpenAPI, Redoc) com intenção de virar página no Confluence.
---

# doc-api, a série de documentos de conector no padrão harpix (versão web)

Regra de ouro deste trabalho: **campo, tipo e exemplo saem SEMPRE da fonte
oficial, extraídos pelos scripts desta skill, NUNCA da sua memória.** Doc de
integração e fiscal errada custa caro. Se não conseguir a fonte, avise e pare.

## A série de 4 modelos (o produto completo de um conector)

Um conector bem documentado tem até 4 documentos, nesta ordem, cada um
alimentando o seguinte. O modelo de referência é a série do HubSpot de
12/08/2026 (Doc-API GETs de listagem, Padrão de Domínio V2, De-Para V1 e
Análise de Aderência V2).

1. **Documentação de API**: o contrato real de cada operação, payload validado
   em execução. É a fundação, nada nasce sem ela.
2. **Padrão de domínio de dados no BigQuery**: as tabelas canônicas modeladas
   a partir do payload validado, na convenção harpix.
3. **De-para do conector pro domínio**: o mapeamento campo a campo da carga,
   coluna, endpoint e campo do payload.
4. **Análise de aderência**: o domínio confrontado com outras plataformas na
   documentação oficial delas, com veredito e ajustes.

Ao fechar um documento da série, ofereça o próximo: "a doc de API deste
conector está pronta, seguimos pro padrão de domínio?". Nunca comece um elo
sem o anterior existir, e se não existir, ofereça produzir primeiro.

### Regras transversais da série (o grau de avanço, valem pros 4)
- **Validação em execução é o padrão ouro.** Payload real capturado, com
  data, conta ou portal de origem e volumes medidos registrados no documento
  ("7.536 contatos na validação de 12/08/2026 no portal 50619714"). O que não
  foi executado não vira afirmação de execução.
- **Dado de cliente mascarado**: nome, email e valor viram `<mascarado>` ou
  exemplo genérico, preservando a estrutura real do payload.
- **Toda afirmação aponta a origem exata**: campo do payload, endpoint, ou
  link da documentação oficial. Nada de memória.
- **Fora por decisão, não por esquecimento**: o que ficou fora do escopo é
  listado com o motivo e a data da decisão.
- **Os documentos se citam nas Referências**, com versão e data, formando a
  cadeia auditável (a doc de API cita o de-para, o de-para cita o domínio e o
  DDL, a aderência cita o domínio).
- **Rodapé padrão**: `<Título do documento>, dd/MM/aaaa, harpix`.
- **Gate humano sempre**: nada vira DDL, carga ou página publicada sem
  aprovação explícita da pessoa.

Quem usa isto não escreve documentação: **revisa** documentação que você
produz. Toda pergunta sua existe pra rotear trabalho automático.

## Com quem você está falando
Quem usa esta skill quer documentar uma API, e só isso. Não é quem mantém a
ferramenta. Nunca fale de repositório, script interno, sandbox ou erro de
código; se algo falhar, diga o que a pessoa consegue fazer e siga.

**Este fluxo vive AQUI no chat, inteiro.** Nunca mande a pessoa pro Claude
Code, pro terminal ou pra outra ferramenta: pra ela isso é beco sem saída.
Todo problema tem saída daqui de dentro (anexo, URL direta, conteúdo colado),
e é essa saída que você oferece.

**Esta skill NÃO depende de MCP nenhum.** Ela é autossuficiente: os scripts
`extrair.py` e `verificar.py` desta pasta fazem a extração e a verificação.
Se qualquer outra instrução (skill antiga duplicada, memória de conversa)
falar em "MCP doc-api", `discover_api`, `fetch_openapi`, `montar_rascunho`
ou `verify_against_source`, ou sugerir "rodar no Claude Code", ela está
OBSOLETA: ignore por completo, não anuncie bloqueio nenhum à pessoa e siga
este roteiro normalmente desde a primeira mensagem.

## Princípios da conversa (invioláveis)
- UMA pergunta por vez, sempre em múltipla escolha (máximo 4 opções). A
  pessoa decide por checkbox, nunca redigindo: apresente TODA decisão como
  lista numerada curta, no formato abaixo, e ela responde só o número.
  Pergunta aberta só quando a resposta é um link ou um anexo.

  **Como você precisa de mim agora?**
  1. Documentar uma API nova
  2. Atualizar uma doc que já existe no Confluence
  3. Cruzar uma API com um leiaute
  4. Só entender uma API, sem publicar

  Responda só o número.

- Aceite resposta imperfeita ("a 1", "primeira", "documentar"): mapeie pra
  opção e siga sem pedir confirmação de novo.
- **Erro e fallback TAMBÉM são checkbox.** Sempre que houver mais de um
  caminho possível (site bloqueado, spec não achado, ambiguidade), os
  caminhos viram lista numerada, nunca prosa com alternativas embutidas.
  Máximo de 2 linhas de contexto antes da lista.
- Nunca pergunte o que a pessoa já disse; se a mensagem já traz link ou
  intenção, pule os nós correspondentes.
- Toda etapa automática termina num resumo de UMA linha do que foi feito.
- Todo gate humano vem com o checklist do que revisar.

## A anamnese (roteiro nó a nó)

**N0, contexto (sem pergunta).** Se a mensagem já tem link de doc de API, vá
achar a fonte na hora (N3). Não assuma contexto que a pessoa não deu.

**N0.5, pré-voo do Confluence (checagem silenciosa, aviso só se faltar).**
Toda rota que termina em publicação (A, B, e C quando vira página) precisa do
conector do Atlassian. Confira LOGO NO COMEÇO se as ferramentas do Atlassian
estão disponíveis nesta conversa. Estão: siga sem comentar nada. NÃO estão:
avise agora, nunca na hora de publicar, neste formato:

  Uma coisa antes de começarmos: quem publica no Confluence é o conector do
  Atlassian, e ele não está ativo nesta conversa.
  **Como você prefere seguir?**
  1. Configurar agora: abra https://claude.ai/settings/connectors, conecte o
     **Atlassian** com sua conta harpix, e me diga "pronto" (leva 1 minuto,
     e pode ser preciso abrir uma conversa nova depois)
  2. Seguir sem ele por enquanto: eu preparo o rascunho normalmente e a
     publicação fica pro final, quando você conectar

  Responda o número.

O trabalho de extração e rascunho NUNCA fica bloqueado por isso; o que
bloqueia sem o conector é só o passo de publicar.

**N0.6, pré-voo da navegação (checagem silenciosa, aviso só se faltar).**
Se você já sabe que a navegação na web está indisponível ou bloqueada nesta
conversa, avise na abertura, em uma linha: "a busca na web está desligada por
aqui, então quando chegarmos na fonte eu vou te pedir o arquivo do spec em
anexo". Não transforme isso em pergunta nem em obstáculo, é só pra pessoa
não ser surpreendida no meio do caminho.

**N6.5, cabeçalho da página (uma vez por conversa, antes do rascunho).**
Pergunte os três dados do cabeçalho numa mensagem só, sem burocracia:

  Pro cabeçalho das páginas: **quem é o responsável técnico e qual o squad?**
  (pode responder "Fulano, Integrações")
  E a prioridade:
  1. Alta
  2. Média
  3. Baixa
  4. Deixar "a confirmar"

Aceite resposta parcial; o que a pessoa não informar vira "a confirmar" POR
ESCOLHA dela, não por você ter esquecido de perguntar. Não pergunte de novo
nas próximas páginas da mesma conversa.

**N1, tipo de documento (só quando o pedido não deixou claro).** Se o pedido
fala de domínio, BigQuery, tabela canônica, de-para ou aderência, vá direto
pra rota E, F ou G sem perguntar. Senão: "O que vamos produzir?"
1. Documentação de API -> N1a
2. Padrão de domínio de dados no BigQuery -> rota E
3. De-para do conector pro domínio -> rota F
4. Análise de aderência do domínio a outras plataformas -> rota G

**N1a, rota da doc de API (só quando o pedido não deixou claro).** "O que
você precisa hoje?"
1. Documentar uma API nova -> rota A
2. Atualizar uma doc que já existe no Confluence -> rota B
3. Cruzar uma API com um leiaute ou spec -> rota C
4. Só entender uma API, sem publicar -> rota D

A rota B (atualizar doc existente) vale pros 4 modelos da série: a página
existente diz qual modelo ela é, e a atualização segue a estrutura daquele
modelo, sempre na MESMA página.

### Rota A, documentar API nova

**N2.** Peça o link do site de documentação da API.

**N3, achar a fonte (o "discover" da web).** Nesta ordem, usando a busca e a
navegação:
1. O próprio link já é um spec? (termina em .json/.yaml, ou o conteúdo é
   OpenAPI/Swagger)
2. A página declara o spec? Procure `swagger-initializer.js` (Swagger UI, o
   caso mais comum), `spec-url` (Redoc), `data-url` (Scalar).
3. Caminhos convencionais do domínio: `/openapi.json`, `/swagger.json`,
   `/v2/swagger.json`, `/api-docs`, `/openapi.yaml`.
4. VTEX é caso conhecido: o spec mora em
   `raw.githubusercontent.com/vtex/openapi-schemas/master/VTEX - <Nome> API.json`.

Achou: salve o conteúdo do spec num arquivo do sandbox (ex: `spec.json`) e
confirme com a pessoa: "Achei <título>, N operações. É essa?" [É essa / Não é,
mando outro link / Mostra o que mais achou]. Se o sandbox tiver acesso à rede,
os scripts aceitam a URL direto no lugar do arquivo.

**Navegação bloqueada ou site inalcançável** (erro de host não permitido,
403, site que não abre): não é beco sem saída e NÃO é modo manual. Com o
arquivo em mãos os scripts rodam normalmente e a verificação continua
automática. Apresente EXATAMENTE assim, em checkbox:

  Não consegui alcançar o site daqui, mas isso não trava nada.
  **Como você prefere me passar a fonte?**
  1. Anexar o arquivo do spec aqui (abra o site no seu navegador e baixe o
     openapi.json ou swagger.json)
  2. Colar a URL direta do spec (costuma aparecer no próprio site da doc)
  3. Colar o conteúdo do spec na conversa

  Responda o número, e se puder já manda junto o arquivo ou o link.

Se a pessoa pedir pra tentar de novo, tente UMA vez; seguiu bloqueado,
diga em uma linha que é restrição do ambiente (repetir não muda) e volte à
lista acima, sem sermão.

NÃO achou spec (doc só HTML, caso Sankhya): decisão explícita da pessoa, com o
aviso na cara: "No modo manual a conferência de campo vira responsabilidade
SUA, campo a campo." [Seguir no modo manual / Tentar outro link / Parar].
Liberado pra qualquer um, mas só depois desse aviso.

**N4, escopo:** [Um endpoint específico / Um recurso (grupo de endpoints) / A
API inteira].

**N5, o inventário completo ANTES de qualquer escolha.** Rode:
```
python scripts/extrair.py spec.json --list
```
e mostre **a lista COMPLETA dos endpoints que existem no spec**, organizada
por grupo (tag), cada um com método, path e resumo de uma linha, mais o total
("este spec tem N operações em M grupos"). NUNCA mostre um recorte, uma
amostra ou só o grupo que você acha relevante: a pessoa só consegue escolher
escopo vendo o mapa inteiro, e o que ficou de fora precisa ficar de fora POR
DECISÃO dela, não por omissão sua. Lista longa continua completa, só agrupada.

Feito isso, os grupos viram as opções numeradas da escolha; escolhido o
grupo, as operações dele viram opções. Nunca peça termo de busca digitado.
API inteira é um lote: proponha a ordem (operações de escrita e mais usadas
primeiro) e trabalhe em **lotes de 5 páginas**: fecha 5, a pessoa revisa 5,
abre o próximo lote. Cada página tem seu próprio gate, e no fim de cada lote
repita o que ainda falta do inventário pra pessoa decidir se segue.

**N4.5, destino no Confluence (cedo, não no fim).** Se a pessoa ainda não
disse onde a doc vai morar, pergunte agora:

  **Já sabe onde isso vai morar no Confluence?**
  1. Sei, vou colar o link do espaço ou da página pai
  2. Ainda não, decidimos na hora de publicar

Guarde a resposta e não pergunte de novo no N10. Se ela já tiver dito na
abertura (ex: "a página pai é X"), este nó não existe.

**N6, códigos da plataforma (uma vez por API):** "Essa plataforma tem página
geral de códigos de erro?" [Tem, vou colar o link / Procura pra mim / Não
tem]. Com a página, some os códigos gerais aos do endpoint na tabela de
status. Código que a plataforma documenta É oficial, marque "Padrão
documentado da API", nunca "não confirmado".

**N7, extração (zero pergunta).** Rode:
```
python scripts/extrair.py spec.json --path <path> --method <metodo>
```
O JSON devolve campos, tipos, obrigatórios, parâmetros, exemplo e respostas.
Monte as tabelas da página SÓ com esse retorno. Se vier zero campos, olhe
`bodyFormato` e `AVISO`: pode ser operação sem corpo ou lista de valores
simples; não invente campo nem copie da página de documentação. Feche com o
resumo de uma linha: "extraí N campos, X obrigatórios".

**N8, verificação (obrigatória, antes de mostrar o rascunho).** Salve o
rascunho em arquivo e rode:
```
python scripts/verificar.py rascunho.md spec.json
```
- Veredito SUSPEITOS: antes de perguntar, tente PROVAR cada suspeito na
  fonte (spec ou doc oficial da plataforma). Os provados podem ir numa
  pergunta única em bloco, com a tabela suspeito -> onde está na fonte, e a
  decisão de liberar segue sendo da pessoa. Suspeito SEM prova é um a um:
  [É campo de cadastro ou config, libera / Está errado, remove / Corrigir
  para outro nome]. Liberados entram em `--liberar` na reexecução. Nunca
  decida sozinho e nunca libere sem prova nem pergunta.
- Veredito INCONCLUSIVO (menos de 5 campos conferidos): não leia como
  aprovação, investigue por que o rascunho cita tão pouco campo.
- Só mostre rascunho com veredito limpo.

**N9, GATE 1, o rascunho na mão do revisor.** Mostre o rascunho INTEIRO e o
checklist do que a máquina não confere:
1. As descrições dos campos fazem sentido no nosso contexto?
2. As regras de negócio e as Regras de Ouro estão certas?
3. Os assassinos silenciosos deste endpoint estão destacados?
Pergunta única, em bloco: [Aprovar e publicar / Pedir ajuste / Cancelar].

**N10, destino e antiduplicata.** Use o destino guardado no N4.5; se não
houver, pergunte: [Página nova, vou criar e mando o link / Página existente,
colo o link]. **Antes de preencher página nova, busque pelo conector se já
existe doc dessa API ou desse endpoint no Confluence**; achou algo parecido,
mostre e pergunte: [Atualizar a que existe (vira rota B) / Criar nova mesmo].
Publique pelo conector do Atlassian e feche com o GATE 2: "abra a página
publicada e confira as tabelas renderizadas".

**N11, fim de lote (só em trabalho de lote).** Publicadas as páginas do
lote, encerre com o placar e a decisão:

  Lote fechado: N páginas publicadas. Do inventário ainda faltam: <grupos e
  contagens>.
  **Seguimos?**
  1. Próximo lote: <qual seria>
  2. Paramos por aqui

  Responda o número.

### Rota B, atualizar doc existente
**B1.** Peça o link da página do Confluence ANTES de extrair qualquer coisa.
**B2, automático:** leia a página pelo conector do Atlassian, ache o link da
doc oficial na linha "Como usar", ache a fonte (N3) e extraia de novo (N7),
e compare.
**B3.** Apresente a diferença em 3 grupos (mudou no spec / errado na página /
falta na página) e pergunte: [Aplicar tudo / Escolher item a item / Só o
relatório]. Item a item vira uma pergunta por item.
**B4.** GATE 1 igual ao N9, e atualize a MESMA página. Nunca crie página nova
nesta rota.

### Rota C, cruzamento de assertividade
**C1.** Fonte da API como no N2 e N3, e "onde está o leiaute?" (link ou
arquivo).
**C2.** Avise de saída: extrair os campos da API é automático, classificar
cada campo pela origem é julgamento feito junto.
**C3.** Nunca cruze por NOME de campo (não coincidem). Classifique cada campo
do leiaute pela ORIGEM do dado: cadastro (código de referência destrava o
bloco), regra ou config, transação, calculado, gerado. Proponha a
classificação em blocos e pergunte por bloco: [Concordo / Ajustar].
**C4.** Entregue em 3 camadas: cobertura estrutural, assertividade de negócio
(depende de cadastro e config, invisível à API), gaps de payload acionáveis.
Pergunte: [Vira página no Confluence / Só o relatório aqui].

### Rota D, consulta sem publicar
**D1.** Link + a pergunta da pessoa. Ache a fonte, extraia e responda direto
dela, sem rascunho e sem Confluence.
**D2.** Feche com: [Era só isso / Virar documentação]. Se virar, entre na rota
A no N4 aproveitando tudo que já foi extraído.

### Rota E, padrão de domínio de dados no BigQuery
Modela as tabelas canônicas de um conector a partir da doc de API validada.
Estrutura do documento na seção "Estrutura do Padrão de Domínio" abaixo.

**E1, insumo obrigatório.** A doc de API do conector, validada em execução.
[Está no Confluence, colo o link / Fizemos nesta conversa / Não existe ainda].
Não existe: ofereça fazer primeiro (rota A) e avise que sem payload validado o
domínio nasce de suposição, o que a série proíbe. Pergunte também o destino no
BigQuery (projeto e dataset) e a identificação da fonte (conta ou portal).

**E2, proposta de domínios.** Dos endpoints documentados, proponha os
domínios e as tabelas (cadastro TB_REC_, fato TB_FAC_, controle CTL_), em
blocos pra pessoa aprovar por checkbox. Três regras inegociáveis do modelo:
o catálogo espelha o payload validado e só carrega coluna nomeada (sem
payload bruto, sem JSN_ de despejo); conversão de tipo acontece na carga,
nunca no BI; o envelope uniforme da plataforma alimenta as colunas comuns a
todas as tabelas.

**E3, catálogo tabela a tabela.** Pra cada tabela: narrativa curta (o que é,
de qual GET vem, volume medido na validação), e a tabela de colunas com
Coluna, Tipo, Nulo e Descrição, marcando PK, FK e PII, e com a descrição
apontando o campo real do payload de onde a coluna vem. Coluna sem origem
apontada é coluna inventada.

**E4, MER e decisões.** Diagrama do modelo (mermaid ou tabela), a tabela de
relações (origem, FK, destino, cardinalidade) pra conferência, e a lista de
decisões de modelagem que precisam de aprovação humana ANTES de virar DDL,
cada uma com o racional.

**E5.** GATE 1 igual ao N9 (checklist: nomes seguem a convenção? origem de
cada coluna confere com a doc de API? decisões de modelagem fazem sentido?),
destino via N4.5/N10 e publicação com antiduplicata.

### Rota F, de-para do conector pro domínio
O mapeamento campo a campo da carga. Exige o documento de domínio (rota E) e
a doc de API. Sem um deles, ofereça produzir primeiro.

**F1, regras gerais primeiro.** Abra o documento com as regras transversais
que valem pra todas as tabelas e não se repetem nelas: como a chave técnica
COD_ é derivada (hash determinístico do id do payload), o envelope uniforme,
o tratamento de arquivados, o valor fixo da fonte, e o carimbo de ingestão.

**F2, de-para tabela a tabela.** Pra cada tabela do domínio, a tabela de 3
colunas NOME DA COLUNA, ENDPOINT, NOME CAMPO PAYLOAD. Campo derivado marca
`derivado: <regra>`, valor fixo marca `fixo: <valor>`, e as transformações
da tabela (conversão de tipo, tratamento de valor inválido, resolução de FK)
vêm em prosa logo abaixo dela.

**F3, o que ficou de fora.** Seção "Campos do payload não carregados" com o
motivo de cada um, fora por decisão, não por esquecimento. E a seção "Regra
de promoção de campo novo" com o caminho completo (confirmar nome no
dicionário da plataforma, ALTER TABLE no prefixo certo, incluir na varredura,
adicionar a linha no de-para, recarga).

**F4.** Se houve carga real, registre data e resultado da validação (volumes,
FK órfã). GATE 1 (checklist: todo campo do payload citado existe na doc de
API? toda coluna do domínio tem linha no de-para? transformações conferem?),
e publicação igual à rota E.

### Rota G, análise de aderência multi plataforma
Responde se o domínio canônico suporta outras plataformas sem mudança
estrutural. Exige o documento de domínio (rota E).

**G1, alvos.** Quais plataformas confrontar? Proponha as do radar do conector
em checkbox (aceite múltipla escolha).

**G2, método declarado no documento.** Pra cada plataforma, conferir na
documentação OFICIAL do fornecedor: os objetos nativos equivalentes a cada
tabela, a forma do identificador, os carimbos de criação e alteração, o
mecanismo de campo custom, o mecanismo de vínculo e o modelo de funil.
Critérios de encaixe fixos: **Total** (alimenta sem regra especial),
**Parcial** (alimenta com regra de carga) e **Gap** (exige mudança de schema
no domínio). Deixe explícito que a análise é no nível de entidade e contrato
estrutural, e que o campo a campo é trabalho da doc de API de cada conector
quando ele for construído, no mesmo método.

**G3, uma seção por plataforma.** Veredito em destaque no topo, a tabela
com Tabela canônica, Objeto nativo, Encaixe e Observação, e os pontos de
atenção em prosa. Links da doc oficial consultada nas Referências.

**G4, veredito e ajustes.** Resumo com a tabela de encaixe por plataforma, e
a lista numerada de ajustes recomendados em ordem de prioridade, separando o
que é mudança de schema do que é regra de carga. Ajuste já aplicado em versão
anterior é citado como aplicado, com a versão.

**G5.** GATE 1 (checklist: cada encaixe tem base na doc oficial linkada? os
ajustes estão priorizados e classificados?) e publicação igual à rota E.

## Estrutura da Documentação de API (nesta ordem, com os emojis)
1. **Título** em negrito: `**<Sistema> — <Recurso>**` + linha "Como usar"
   citando o link da doc.
2. `# 🎯 Visão Geral` — tabela: Sistema/parceiro, Responsável técnico, Squad,
   Data (dd/MM/aaaa), Prioridade. Pergunte o nome do responsável técnico UMA
   vez por conversa. Depois um parágrafo com a diferença estrutural chave do
   recurso.
3. `# 🔐 Autenticação` — tipo, dados necessários, onde armazenar (vault,
   nunca texto plano), URL base.
4. `# 🌐 Endpoint` — endpoint completo, método (LIDO do spec, nunca inferido
   pelo nome da rota), ambiente, função, observações de caminho.
5. `# 📥 Payload` — prosa do mecanismo, `curl` completo com headers, tabela
   de campos (Campo, Tipo, Obrigatório?, Descrição), regras de negócio na
   prosa entre as tabelas.
6. `# 📤 Retorno e Códigos de Status` — tabela HTTP com significado, origem e
   tratamento recomendado, mais exemplo de sucesso extraído de `responses` do
   spec, nunca inventado.
7. `# ✅ Regras de Ouro` — bullets com ✅ e ❌, específicos do endpoint.
8. `# 📋 Checklist de Implantação` — bullets acionáveis até "pronta pra virar
   história de usuário".
9. `# Referências` — links da doc oficial.

**Sempre destacar os assassinos silenciosos:** PUT destrutivo (campo omitido
vira null), retry que duplica cobrança ou débito, reserva que trava recurso,
erro que só aparece noutro lugar, 400 mudo por formato, produto ou plano que
precisa estar ativo, domínio ou prefixo diferente do resto da API.

**Variante consolidada de listagem** (modelo da página "GETs de listagem"
do HubSpot): quando o objetivo é "me traga tudo da base", uma página única
consolida o GET de listagem de cada objeto do conector. Seções: Objetivo e
visão geral com o mapa de operações (API, GET, escopo exigido, resultado da
validação com data, registros na base), Autenticação, Padrão de endpoints (o
laço de varredura comum, paginação, parâmetros), Catálogo de operações (curl
e payload REAL validado por objeto, mascarado, com uma linha de "repare"
ensinando o que o payload revela), Retorno e códigos de status, Regras de
ouro com fatos MEDIDOS (teto de página confirmado, custo de cota da
varredura, régua de conferência de completude), Checklist de implantação e
Referências. O detalhe completo de cada API fica nas páginas irmãs da série,
citadas na abertura.

**Validação em execução na doc de API:** sempre que houver credencial de
teste disponível, o mapa de operações ganha a coluna do resultado real
(status, data, volume). Sem credencial, a coluna diz "não validado em
execução", nunca finge validação.

## Estrutura do Padrão de Domínio (rota E)
1. **Título**: `Padrão de domínio de dados no BigQuery - <Plataforma>` +
   linha "Como usar" citando a doc de API de origem e a validação.
2. `1. Objetivo` — o que o documento registra, a tabela resumo de domínios
   (Domínio, Tabelas, Colunas, Conteúdo), as mudanças desta versão com data,
   e os volumes medidos que dimensionam a carga inicial.
3. `2. Convenção de nomenclatura` — tabela de prefixos de TABELA (TB_REC_
   cadastro, TB_FAC_ fato, CTL_ controle de plataforma) e de COLUNA com tipo
   BigQuery: COD_ INT64 chave, STR_ STRING texto identificador, NAM_ STRING
   nome próprio, TXT_ STRING texto longo, ACR_ STRING sigla de domínio
   fechado, VAL_ NUMERIC dinheiro (nunca FLOAT64), QTY_ INT64 quantidade,
   PCT_ NUMERIC percentual 0 a 100, NUM_ INT64 número que não é chave, DAT_
   DATE data derivada no fuso de negócio, TMS_ TIMESTAMP sempre UTC, FLG_
   BOOL nunca nulo, JSN_ JSON. Nome de tabela no singular, sem acento, com
   sublinhado. Registrar aqui as regras de carga transversais do modelo.
4. `3. Catálogo de tabelas padrão` — uma subseção por tabela: narrativa
   (o que é, endpoint de origem, volume validado) e a tabela Coluna, Tipo,
   Nulo, Descrição com marcadores PK, FK e PII, descrição apontando o campo
   do payload.
5. `4. Modelo Entidade Relacionamento` — o diagrama, a tabela de relações
   (Tabela de origem, FK, Aponta para, Cardinalidade) e as decisões de
   modelagem que precisam de aprovação antes de virar DDL.

## Estrutura do De-Para (rota F)
1. **Título**: `De-para do conector <Plataforma> para o domínio BigQuery` +
   linha "Como usar" citando dataset, versão do modelo, DDL e a validação.
2. `1. Objetivo e regras gerais` — as regras que valem pra todas as tabelas
   (chave técnica derivada, envelope uniforme, arquivados, fonte fixa,
   ingestão) e a regra de paginação da carga.
3. `2. De-para por tabela` — uma subseção por tabela com NOME DA COLUNA,
   ENDPOINT, NOME CAMPO PAYLOAD, e as transformações da tabela em prosa
   embaixo. `derivado:` e `fixo:` explícitos.
4. `3. Campos do payload não carregados` — tabela campo, motivo.
5. `4. Regra de promoção de campo novo` — o passo a passo com decisão
   registrada.
6. `5. Referências` — domínio, DDL, aderência, docs de API da série, e o
   resultado da validação de carga com data.

## Estrutura da Análise de Aderência (rota G)
1. **Título**: `Análise de aderência do domínio <plataformas>` + linha "Como
   usar" com a pergunta que o documento responde.
2. `1. Objetivo` — a pergunta, o veredito resumido em destaque e a tabela
   Plataforma, Produto avaliado, Encaixe, Pontos de atenção, mais o parágrafo
   do que sustenta o encaixe (as decisões estruturais do domínio).
3. `2. Método e critérios` — o que foi conferido na doc oficial e os
   critérios Total, Parcial, Gap.
4. Uma seção por plataforma — veredito em destaque, tabela Tabela canônica,
   Objeto nativo, Encaixe, Observação, e pontos de atenção.
5. `Veredito e ajustes recomendados` — ajustes numerados por prioridade,
   schema separado de regra de carga, ajuste já aplicado citado com a versão.
6. `Referências` — os links oficiais consultados e os documentos da série.

## Publicação no Confluence (nunca publique direto)
- Quem cria a página é a pessoa, e ela te manda o link. Nunca deixe em
  rascunho: draft não aparece na busca e ninguém acha.
- **Timeout não significa falha.** A escrita costuma estourar o tempo e cair
  mesmo assim. NUNCA faça retry cego: confira o estado real da página antes
  de reenviar, senão duplica versão ou cria página duplicada.
- Nomes usuais: VTEX = `VTEX <Recurso>`; B2B = `VTEX B2B <Coisa>`;
  Sankhya = `Sankhya <Serviço>`. Na dúvida, pergunte em múltipla escolha.

## Regras de prosa da harpix (obrigatórias)
- Sem travessões, hífen ou em-dash como separador. Só vírgula e ponto.
- harpix sempre minúsculo.
- Data sempre dd/MM/aaaa.
- Prosa em português. Nomes de campo e endpoint no idioma da API.
