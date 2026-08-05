# Documentação de API na harpix, manual do processo

Responsável pelo processo: Guilherme Teixeira. Última revisão: 05/08/2026. Versão da skill: a publicada no harpix go.

Este manual é a fonte única do processo de documentação de API da harpix. Ele existe pra que o processo funcione igual pra qualquer pessoa do time, hoje e depois de qualquer troca de pessoas. Se algo aqui contradiz o que alguém lembra de cabeça, vale o manual.

## 1. O processo em uma página

Documentar uma API na harpix é transformar a documentação pública de um parceiro (HubSpot, VTEX, Sankhya, Bling, qualquer outro) numa página do Confluence no padrão harpix, com todos os campos, tipos e obrigatoriedades extraídos da fonte oficial e conferidos por código.

O princípio que sustenta tudo: **campo, tipo e exemplo saem sempre da fonte oficial, nunca da memória de quem escreve, nem da memória da IA.** Documentação de integração errada custa caro no cliente.

Onde isso acontece: **no chat padrão do Claude (claude.ai)**, com a skill doc-api instalada. Sem terminal, sem programa instalado, sem conhecimento técnico prévio. A pessoa conversa, decide por perguntas de múltipla escolha respondendo só o número, e a única coisa que digita é link (ou anexa um arquivo).

O fluxo, com os dois gates humanos marcados:

```
link da doc do parceiro (ou arquivo do spec anexado)
        |
  [fonte] a skill acha o OpenAPI por trás do site
        |
  [inventário] a lista COMPLETA de endpoints, pra escolher escopo vendo tudo
        |
  [extração] campos, tipos, obrigatórios, por script, direto do spec
        |
  [rascunho] a página no padrão harpix
        |
  [verificação] todo campo citado é conferido por script contra a fonte
        |
  GATE 1: a pessoa lê e aprova o rascunho
        |
  [publicação] na página do Confluence, pela conta da pessoa
        |
  GATE 2: revisão na página publicada
```

A divisão de trabalho é fixa: os **scripts** extraem e conferem, o **Claude** conduz e redige no padrão, a **pessoa** decide e aprova. O papel humano é de **revisor**: nada é publicado sem os dois gates, e ninguém digita tabela de campo na mão.

## 2. Papéis e responsabilidades

| Papel | Quem | O que faz |
|---|---|---|
| Operador | qualquer pessoa do time | conduz a documentação no chat, aprova o rascunho, publica com a própria conta |
| Revisor | um par técnico | lê a página publicada, confere descrição e regra de negócio (a máquina confere campo, não verdade) |
| Dono do processo | Guilherme Teixeira | mantém a skill, o padrão de página e este manual; recebe reporte de problema |

Duas regras de sucessão, pra este processo nunca depender de uma pessoa:

1. O padrão de página e o roteiro da conversa não moram na cabeça de ninguém, moram dentro da skill (o arquivo que todo mundo baixa do harpix go) e neste manual. Mudança de padrão é versão nova da skill no go, que chega igual pra todo mundo.
2. Quando o dono do processo mudar, muda a linha desta tabela e nada mais. Todo o conhecimento operacional está aqui, no manual do usuário e na própria skill.

## 3. Preparar o acesso (uma vez por pessoa)

O passo a passo completo, com telas e socorro, está no **manual do usuário** (também no harpix go). O resumo é o checklist dos 3 sins:

1. A skill **doc-api** aparece em Configurações > Recursos > Skills do claude.ai? Não: baixar o zip no harpix go e inserir.
2. O conector **Atlassian** está conectado? Não: `claude.ai/settings/connectors`.
3. Consigo **escrever no espaço do Confluence** onde a doc vai morar? Não: permissão com quem administra o Atlassian.

Três sins e a pessoa nunca mais volta nesse checklist. A própria skill confere o conector e a navegação no início de cada trabalho e avisa com o atalho certo se algo faltar, sem travar o rascunho.

## 4. O fluxo passo a passo

A pessoa abre uma conversa e diz o que precisa, do seu jeito ("quero documentar essa API: <link>"). A skill conduz por perguntas numeradas. O roteiro por trás:

**Primeiro, a rota.** O que a pessoa precisa define o caminho:

| Rota | Quando | O que muda |
|---|---|---|
| A. Documentar API nova | o caso principal | fluxo completo abaixo |
| B. Atualizar doc existente | a página já está no Confluence | a skill lê a página primeiro, reextrai do spec e propõe a diferença em 3 grupos; nunca cria página nova |
| C. Cruzar API com leiaute | análise de assertividade | classificação por origem do dado, feita em conjunto |
| D. Só entender uma API | consulta sem publicar | extração e resposta, sem rascunho nem Confluence |

**Na rota A, a sequência:**

1. **Fonte.** A pessoa cola o link do site de documentação. A skill procura o OpenAPI por trás do site; se a navegação estiver bloqueada, pede o arquivo do spec em anexo (baixado do site no navegador da pessoa), e nada se perde: a extração continua automática. Se a API não tiver spec nenhum (caso Sankhya), a skill avisa na cara e o modo manual só segue com decisão explícita da pessoa, sabendo que a conferência de campo vira responsabilidade dela.
2. **Inventário completo.** Antes de qualquer escolha, a lista inteira de endpoints do spec, agrupada, com o total. O que fica de fora da doc fica de fora por decisão da pessoa, nunca por omissão.
3. **Escopo.** Um endpoint, um recurso, ou a API inteira. API inteira vira lotes de 5 páginas, cada página com seu gate, e ao fim de cada lote a skill mostra o que ainda falta do inventário e pergunta se segue.
4. **Destino.** Onde a doc vai morar no Confluence é perguntado cedo (espaço ou página pai), não na hora de publicar.
5. **Cabeçalho.** Responsável técnico, squad e prioridade, perguntados uma vez por conversa. "A confirmar" só existe por escolha da pessoa.
6. **Extração e rascunho.** Automáticos, por script. Zero campos nunca é resposta calada: a skill explica o formato do corpo ou avisa que a extração falhou, e ninguém preenche de memória.
7. **Verificação.** Todo campo citado no rascunho é conferido por script contra o spec. Suspeito com prova na fonte vem numa pergunta em bloco com a tabela de prova; suspeito sem prova é decidido um a um pela pessoa. Menos de 5 campos conferidos é veredito inconclusivo, não aprovação.
8. **GATE 1.** O rascunho inteiro na mão da pessoa, com o checklist do que a máquina não confere: as descrições fazem sentido? as regras de negócio e as Regras de Ouro estão certas? os assassinos silenciosos estão destacados?
9. **Publicação.** Antes de criar página nova, a skill busca se já existe doc daquela API no Confluence, pra não nascer duplicata. A pessoa cria a página (publicada, nunca rascunho), manda o link, e a skill preenche pela conta dela.
10. **GATE 2.** Abrir a página publicada e conferir as tabelas renderizadas. De preferência, um par revisa também.

## 5. O padrão de página harpix

Toda página tem as mesmas 9 seções, nesta ordem, com os emojis nos títulos:

1. **Título** em negrito, `**<Sistema> — <Recurso>**`, e a linha "Como usar" citando o link da doc oficial.
2. `🎯 Visão Geral`, tabela com sistema, responsável técnico, squad, data (dd/MM/aaaa) e prioridade, mais um parágrafo com a diferença estrutural chave do recurso.
3. `🔐 Autenticação`, tipo, dados necessários, onde armazenar (vault, nunca texto plano), URL base.
4. `🌐 Endpoint`, endpoint completo, método (lido do spec, nunca inferido pelo nome da rota), ambiente, função, observações de caminho.
5. `📥 Payload`, prosa do mecanismo, `curl` completo com headers, tabela de campos (Campo, Tipo, Obrigatório?, Descrição), e as regras de negócio na prosa entre as tabelas.
6. `📤 Retorno e Códigos de Status`, tabela HTTP com significado, origem e tratamento recomendado, mais exemplo de sucesso extraído do spec. Código documentado pela plataforma é oficial, não "a confirmar".
7. `✅ Regras de Ouro`, bullets com ✅ e ❌, específicos do endpoint, nunca genéricos.
8. `📋 Checklist de Implantação`, bullets acionáveis até "pronta pra virar história de usuário".
9. `Referências`, links da doc oficial.

**Os assassinos silenciosos sempre ganham destaque**: PUT destrutivo (campo omitido vira null), retry que duplica cobrança ou registro, reserva que trava recurso, erro que só aparece em outro lugar, 400 mudo por formato, produto ou plano que precisa estar ativo, domínio diferente do resto da API.

**Prosa harpix**: sem travessões como separador (só vírgula e ponto), harpix minúsculo, data dd/MM/aaaa, prosa em português com nomes de campo no idioma da API.

## 6. Casos especiais

**Site bloqueado pra navegação do Claude.** Não é beco sem saída e não é modo manual: a pessoa baixa o arquivo do spec no navegador dela e anexa na conversa. A extração e a verificação continuam automáticas, idênticas.

**API sem OpenAPI (Sankhya).** A doc é lida da página oficial e o dicionário de tabelas do fornecedor vira a referência de conferência. Sem spec não existe verificação automática, então cada campo é conferido na mão antes do gate 1, e o manual dobra a atenção da revisão.

**Cruzamento de assertividade (rota C).** Nunca cruzar por nome de campo, os nomes não coincidem entre API e leiaute. Cruza-se por origem do dado: cadastro, regra ou config, transação, calculado, gerado. A entrega tem 3 camadas: cobertura estrutural, assertividade de negócio e gaps de payload acionáveis.

**PDF da documentação.** A skill gera quando pedido, direto na conversa. Detalhe conhecido: o ambiente não tem fonte de emoji, então no PDF os emojis dos títulos viram rótulos de texto, e a versão com emoji segue no markdown que vai pro Confluence.

## 7. Erros que já aconteceram, e a regra que ficou

| O que aconteceu | A regra que ficou |
|---|---|
| Timeout na publicação, e a página gravou mesmo assim | nunca republicar no timeout sem conferir a página primeiro; retry cego duplica conteúdo |
| Endpoint devolvia zero campos em silêncio (composição `allOf`, corpo em lista, Swagger 2.0) e a doc saiu incompleta | zero campo nunca é resposta aceitável sem explicação; a extração avisa o formato, e ninguém preenche de memória |
| A verificação aprovava rascunho tendo conferido quase nada | veredito com menos de 5 campos conferidos é inconclusivo, não aprovado |
| Identificadores legítimos (escopo OAuth, host, esquema de auth) acusados como campo inventado | o verificador varre também autenticação, servidores e códigos de resposta; suspeito provado na fonte vai em bloco com a prova |
| A doc saiu de um bloco de endpoints sem a pessoa ver o resto que existia | inventário completo antes de qualquer escolha de escopo, sempre |
| Método HTTP escrito por inferência do nome da rota, e estava errado | método HTTP se lê no spec, sempre |
| Corpo de resposta inventado de cabeça | retorno se extrai de `responses` do spec, com o exemplo oficial |
| Página criada em rascunho no Confluence, e ninguém achava | página nunca fica em rascunho, draft não aparece na busca |
| Fluxo mandava o usuário "resolver no Claude Code" | o fluxo vive inteiro no chat; toda saída oferecida é de dentro da conversa |

## 8. Governança

**Como o processo melhora.** Todo problema real vira regra escrita: o operador manda o print ou o texto da conversa pro dono do processo, a causa vira ajuste na skill ou neste manual, e a versão nova sobe no harpix go. Foi assim que nasceram várias regras da tabela acima, em ciclos de teste real feitos no próprio dia.

**Versão da skill.** A verdade é o zip publicado no harpix go. Quando sai versão nova, o go avisa e cada pessoa troca o arquivo (remover a skill antiga, subir a nova, leva um minuto). Ninguém precisa descobrir mudança de padrão por conta própria: a skill nova já conduz do jeito novo.

**Reporte de problema.** Deu erro, comportamento estranho, resultado incompleto: print da tela + o que você tentou, pro dono do processo. Sem reporte o defeito atinge o próximo colega.

**Onboarding de gente nova.** O caminho tem 4 degraus: (1) ler o manual do usuário e fazer o checklist dos 3 sins; (2) assistir uma documentação sendo feita por alguém experiente; (3) fazer a primeira com um par revisando o gate 1 e o gate 2; (4) autonomia. A meta é a primeira página publicada na primeira semana.
