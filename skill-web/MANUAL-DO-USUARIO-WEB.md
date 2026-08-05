# doc-api no chat do Claude, manual do usuário

Este é o manual de quem vai **documentar API pelo chat padrão do Claude
(claude.ai no navegador)**. Não precisa de terminal, não precisa instalar
programa, não precisa saber o que é OpenAPI. São 3 partes: pegar o arquivo,
inserir no Claude, e usar no dia a dia.

## Parte 1: pegar o arquivo no harpix go

1. Entre no harpix go e vá na página do **doc-api**.
2. Baixe o arquivo **`doc-api-web.zip`**. É um arquivo pequeno, guarda ele na
   pasta Downloads mesmo.
3. Não descompacte. O Claude recebe o zip fechado, do jeito que baixou.

Esse arquivo é a "skill": o pacote com o método de documentação da harpix e
os verificadores que impedem campo inventado. Quando sair versão nova, o go
avisa e o caminho é o mesmo: baixar e inserir de novo.

## Parte 2: inserir no Claude (uma vez só)

1. Abra **claude.ai** no navegador e faça login com a sua conta harpix.
2. Clique no seu avatar (canto inferior esquerdo) e abra **Configurações**
   (Settings).
3. Procure a seção **Recursos** (Capabilities). Confira que **Execução de
   código** (Code execution) está LIGADA. Sem ela os verificadores não rodam.
4. Na mesma área, procure **Skills** e clique em **Enviar skill** (Upload
   skill). Selecione o `doc-api-web.zip` que você baixou.
5. Confirme que a skill **doc-api** aparece na lista, ativada.

Pronto. Isso não se repete: a skill fica na sua conta.

> Não achou a opção de Skills ou de Execução de código? Isso é habilitação do
> plano da empresa, não erro seu. Fale com o dono do processo (Guilherme
> Teixeira), a habilitação é feita pela administração da organização em
> minutos.

Falta só uma peça, o **conector do Atlassian**, que é quem publica no
Confluence com a sua conta: em Configurações > **Conectores**, conecte o
**Atlassian** e faça o login no navegador com a conta harpix. Quem já usa o
Atlassian no Claude (pra Jira, por exemplo) não precisa fazer nada.

## Antes do primeiro uso: o checklist dos 3 sins

Responda sim ou não, na ordem. O primeiro "não" te diz exatamente pra onde ir,
resolve e volta pra pergunta seguinte.

| # | Pergunta | Se NÃO, o caminho |
|---|---|---|
| 1 | A skill **doc-api** aparece em Configurações > Recursos > Skills? | volte à Parte 1 e Parte 2 deste manual (baixar o zip no go e inserir) |
| 2 | O conector **Atlassian** está conectado? | https://claude.ai/settings/connectors, conectar Atlassian com a conta harpix |
| 3 | Consigo escrever no espaço do Confluence onde a doc vai morar? | permissão de Confluence, fale com quem administra o Atlassian na harpix |

Três sins: você está pronto, e nunca mais precisa olhar este checklist. Na
dúvida durante o uso, a própria skill confere o Atlassian e a navegação e te
avisa com o atalho certo.

## Parte 3: usar no dia a dia

1. Abra uma conversa nova no claude.ai.
2. Diga o que precisa, do seu jeito. Exemplos que funcionam:
   - "quero documentar essa API: https://developers.exemplo.com/docs"
   - "documenta o endpoint de criar pedido do parceiro X"
   - "atualiza a doc do Confluence dessa API, aqui o link da página"
3. A partir daí o Claude conduz por **perguntas de múltipla escolha**. Você
   não digita tabela, não digita campo, não decora comando. A única coisa que
   você cola é link.
4. Em algum momento o Claude te mostra o **rascunho pronto** e para. Esse é o
   seu momento: **leia de verdade**. A máquina garante que nenhum campo foi
   inventado, mas só você sabe se as descrições e as regras de negócio fazem
   sentido.
5. Aprovou? Você cria a página no Confluence (publicada, nunca rascunho),
   manda o link, e o Claude preenche pela sua conta. Depois abra a página e
   confira o resultado final.

### As 3 regras que não se negocia

1. **Nada de memória.** Se o Claude disser que não achou a fonte oficial da
   API, o trabalho para ali. Não deixe ele "completar" de cabeça, e não
   complete você.
2. **Nada publica sem você aprovar.** O rascunho sempre para na sua mão antes
   do Confluence.
3. **Timeout na publicação não é falha.** Se o Claude avisar que estourou o
   tempo, ele mesmo confere antes de reenviar. Não mande "tenta de novo" por
   conta própria, republicar às cegas duplica conteúdo.

### Deu problema

| O que aconteceu | O que fazer |
|---|---|
| O Claude diz que não consegue rodar os verificadores | Execução de código está desligada: Configurações > Recursos > ligue Code execution |
| A skill não aparece ou não dispara | confira em Configurações > Skills que a doc-api está na lista e ativada; se não estiver, repita a Parte 2 |
| Erro ao publicar no Confluence | o conector do Atlassian caiu: Configurações > Conectores, conecte de novo |
| Não consegue escrever num espaço do Confluence | é permissão da sua conta no Atlassian, fale com quem administra o Confluence |
| Qualquer outra coisa | print da tela + o que você tentou, pro dono do processo (Guilherme Teixeira) |
