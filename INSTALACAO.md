# doc-api, manual de instalação do zero

Este manual assume que você não tem NADA instalado. Cada passo diz o que fazer,
o que você deve ver quando der certo, e o que fazer quando não der. Siga na
ordem e não pule a verificação final.

## Antes de começar: onde o doc-api funciona

Isso importa mais que qualquer passo abaixo, então leia primeiro.

| Onde você usa o Claude | Funciona? | O que fazer |
|---|---|---|
| **Claude Code** (terminal ou app com terminal) | **Sim, é o caminho** | siga a Parte 1 |
| **Claude Desktop** (aplicativo de chat no computador) | Sim, por outro caminho | siga a Parte 2 |
| **claude.ai no navegador** (o chat padrão da web) | **Não** | veja a Parte 3 |
| **Celular** | Não | veja a Parte 3 |

O motivo: o doc-api roda como um programa na sua máquina. O chat da web e o
celular não têm onde rodar esse programa. Não é configuração que resolve, e
ninguém precisa tentar, já tentamos. A versão que funciona na web está no
roadmap (servidor remoto), mas hoje não existe.

---

## Parte 1: instalar no Claude Code (o caminho recomendado)

### Passo 1.1: conferir se você tem o Node

O doc-api precisa do Node 18 ou superior. Abra um terminal (no Windows,
procure "PowerShell" no menu iniciar) e digite:

```
node -v
```

**O que você deve ver:** algo como `v20.11.0`. Qualquer número de 18 pra cima
serve. Pule pro passo 1.2.

**Se apareceu erro** ("não é reconhecido como comando"): você não tem o Node.
Baixe em https://nodejs.org (botão LTS), rode o instalador com as opções
padrão, feche e abra o terminal de novo, e repita o `node -v`.

> Máquina gerida pela empresa que pede senha de administrador no instalador:
> abra chamado pro TI pedindo "instalação do Node.js LTS". É instalação comum,
> o TI conhece.

### Passo 1.2: conferir se você tem o Claude Code

No mesmo terminal:

```
claude --version
```

**O que você deve ver:** um número de versão. Pule pro passo 1.3.

**Se apareceu erro:** instale com:

```
npm install -g @anthropic-ai/claude-code
```

Depois rode `claude` uma vez e faça o login com a sua conta Claude da harpix
quando ele pedir (abre o navegador).

### Passo 1.3: instalar o plugin

Abra o Claude Code (digite `claude` no terminal) e, dentro dele, rode os dois
comandos, um de cada vez:

```
/plugin marketplace add harpix-Guilherme-Teixeira/hpx-documentador-api
/plugin install doc-api@hpx-documentador-api
```

**O que você deve ver:** confirmação de marketplace adicionado e de plugin
instalado.

### Passo 1.4: REINICIAR o Claude Code (não pule)

Feche o Claude Code (`/exit` ou fechar o terminal) e abra de novo.

Esse passo existe porque a parte de conversa do plugin carrega na hora, mas o
motor (o servidor MCP) **só conecta quando o Claude Code abre**. Sem
reiniciar, o Claude até responde sobre documentação, mas sem as ferramentas de
extração, e ele vai te avisar que está manco.

### Passo 1.5: conectar o Atlassian (quem publica no Confluence)

No Claude Code, digite `/mcp`. Na lista, adicione ou conecte o **Atlassian**.
Ele abre o navegador pra você logar com a sua conta harpix e autorizar. Você
não digita token em lugar nenhum, e se alguém te mandar um API token do
Confluence, não use.

### Passo 1.6: verificação final (o checklist dos 3 sins)

1. `/mcp` mostra **doc-api** conectado? (aparece como `doc-api` ou
   `plugin:doc-api:doc-api`)
2. `/mcp` mostra **Atlassian** conectado?
3. `/doc-api:documentar` existe quando você digita `/doc`?

Três sins: pronto, cole o link de uma documentação de API e vá. Algum não:
tabela de socorro no fim.

### Se você já usava o doc-api antes do plugin

Quem instalou pelo comando antigo (`npx -y hpx-doc-api-mcp setup`) tem um
registro que **esconde** o do plugin. Remova com:

```
claude mcp remove doc-api -s user
```

e reinicie o Claude Code. Fica só o do plugin, que se atualiza sozinho.

---

## Parte 2: instalar no Claude Desktop

O Desktop não tem plugin, mas tem o mesmo motor por outro caminho. No
terminal (não no Desktop):

```
npx -y hpx-doc-api-mcp@latest setup
```

Ele pergunta seu nome (é pra telemetria interna, uma vez só) e registra tudo.
Depois **feche e abra o Claude Desktop**, porque ele só lê a configuração na
abertura. Confira no clipe de ferramentas que o doc-api aparece.

O conector do Atlassian no Desktop: Configurações > Conectores > Atlassian >
Conectar, login no navegador.

---

## Parte 3: você usa o chat da web (claude.ai) ou o celular

Hoje o doc-api **não funciona aí**, e não é falta de configuração, é
arquitetura (o motor roda na sua máquina, e o chat da web não alcança a sua
máquina). O que fazer:

1. **Use o Claude Code pra documentar API.** É a mesma conta, o mesmo Claude,
   com o motor do lado. A Parte 1 te deixa pronto em 10 minutos.
2. Se você nunca usou terminal e travou em qualquer passo, chame o dono do
   processo (Guilherme Teixeira), a instalação assistida leva 5 minutos.
3. A versão pra web (conector remoto) está no roadmap. Quando existir, este
   manual ganha a Parte 4 e o time é avisado.

O que NÃO fazer: pedir pro Claude da web documentar API "de memória". Sem o
motor não há extração da fonte nem verificação de campo inventado, que é
justamente o motivo desse processo existir.

---

## Tabela de socorro

| Sintoma | Causa provável | Ação |
|---|---|---|
| `/mcp` não mostra o doc-api | não reiniciou depois de instalar | feche e abra o Claude Code |
| doc-api aparece mas "failed" | Node ausente ou antigo | `node -v` no terminal; precisa 18+ |
| `/doc-api:documentar` não existe | plugin não instalou | repita o passo 1.3 e olhe a mensagem de erro |
| o Claude diz que não tem as ferramentas de extração | sessão aberta antes do restart, ou você está na web | reinicie o Claude Code; na web não funciona (Parte 3) |
| tinha doc-api antes e algo está estranho | registro antigo escondendo o do plugin | `claude mcp remove doc-api -s user` e reinicie |
| erro ao publicar no Confluence | sessão do Atlassian caiu | `/mcp`, reconecte o Atlassian, login de novo |
| não consegue escrever num espaço do Confluence | permissão da sua conta | fale com quem administra o Confluence; nenhuma config contorna, de propósito |
| instalador do Node pede senha de admin | máquina gerida | chamado pro TI: "instalar Node.js LTS" |

Qualquer coisa fora da tabela: print da tela + o que você tentou, pro dono do
processo. Todo problema real vira melhoria deste manual.
