---
name: doc-api
description: Documenta um endpoint ou uma API inteira no Confluence da harpix no padrão consolidado, extraindo campo, tipo e obrigatoriedade da fonte oficial por script, nunca de memória. Use SEMPRE que o usuário disser "doc-api", "documentar a API X", "documentar o endpoint Y", "fazer a doc dessa API", "atualizar a doc da API", "cruzar a API com o leiaute", ou trouxer um link de documentação de API (developer.*, developers.*, swagger, OpenAPI, Redoc) com intenção de virar página no Confluence.
---

# doc-api, documentação de API no padrão harpix (versão web)

Regra de ouro deste trabalho: **campo, tipo e exemplo saem SEMPRE da fonte
oficial, extraídos pelos scripts desta skill, NUNCA da sua memória.** Doc de
integração e fiscal errada custa caro. Se não conseguir a fonte, avise e pare.

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

**N1, rota (só quando o pedido não deixou claro).** "O que você precisa hoje?"
1. Documentar uma API nova -> rota A
2. Atualizar uma doc que já existe no Confluence -> rota B
3. Cruzar uma API com um leiaute ou spec -> rota C
4. Só entender uma API, sem publicar -> rota D

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

**N5, seleção sem digitação.** Rode:
```
python scripts/extrair.py spec.json --tags
```
e as tags viram as opções da pergunta. Escolhida a área, rode `--list`, filtre
pela tag e as operações viram opções. Nunca peça termo de busca digitado.
API inteira é um lote: proponha a ordem (operações de escrita e mais usadas
primeiro) e trabalhe em **lotes de 5 páginas**: fecha 5, a pessoa revisa 5,
abre o próximo lote. Cada página tem seu próprio gate.

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
- Veredito SUSPEITOS: para CADA campo suspeito, uma pergunta: [É campo de
  cadastro ou config, libera / Está errado, remove / Corrigir para outro
  nome]. Liberados entram em `--liberar` na reexecução. Nunca decida sozinho
  e nunca agrupe suspeitos numa pergunta só.
- Veredito INCONCLUSIVO (menos de 5 campos conferidos): não leia como
  aprovação, investigue por que o rascunho cita tão pouco campo.
- Só mostre rascunho com veredito limpo.

**N9, GATE 1, o rascunho na mão do revisor.** Mostre o rascunho INTEIRO e o
checklist do que a máquina não confere:
1. As descrições dos campos fazem sentido no nosso contexto?
2. As regras de negócio e as Regras de Ouro estão certas?
3. Os assassinos silenciosos deste endpoint estão destacados?
Pergunta única, em bloco: [Aprovar e publicar / Pedir ajuste / Cancelar].

**N10, destino:** [Página nova, vou criar e mando o link / Página existente,
colo o link]. Publique pelo conector do Atlassian e feche com o GATE 2: "abra
a página publicada e confira as tabelas renderizadas".

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

## Estrutura de seção da página (nesta ordem, com os emojis)
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
