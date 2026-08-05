#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A joia do doc-api: confere todo campo citado num rascunho contra o spec.

Porta fiel do verify_against_source do motor. Regras que pagam bugs reais:
 - Le crases, PRIMEIRA COLUNA de tabela markdown e chaves de JSON. So crase
   ignorava justamente a tabela de campos (1 campo conferido num doc de 18).
 - A FONTE decide o que e campo, nunca a lista de ruido. Filtrar por palavra
   antes escondia campo real ("tipo" e obrigatorio no Bling e era pulado por
   parecer cabecalho). Falso negativo em verificador passa como APROVADO.
 - Menos de 5 campos conferidos = INCONCLUSIVO, nao OK. Confianca falsa e
   pior que nao verificar.

Uso:
  python verificar.py rascunho.md spec.json
  python verificar.py rascunho.md spec.json --liberar codigoLoja,idContato

Saida em JSON: veredito OK / SUSPEITOS / INCONCLUSIVO + listas.
"""
import argparse
import json
import re
import sys

from extrair import carregar  # mesmo diretorio

RUIDO = {
    "string", "integer", "number", "boolean", "object", "array", "null", "true", "false",
    "json", "application", "date", "datetime", "float", "double", "long", "int", "uuid",
    "campo", "tipo", "obrigatorio", "descricao", "valor", "item", "sim", "nao", "n/a",
    "get", "post", "put", "patch", "delete", "http", "https", "curl", "bash", "preencher",
    "endpoint", "metodo", "ambiente", "funcao", "alteracao", "parametro", "onde",
    "sistema", "parceiro", "squad", "data", "prioridade", "responsavel", "tecnico",
    # rotulos de tabela chave/valor do padrao harpix (caso real: "Alternativa"
    # numa tabela de autenticacao acusado como campo inventado)
    "alternativa", "exemplo", "observacao", "observacoes", "retorno", "resposta",
    "escopo", "credenciais",
}

NOME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]*$")


def eh_nome_de_campo(tok):
    if not tok or len(tok) < 2 or len(tok) > 60:
        return False
    if tok[0].isdigit():
        return False
    if "/" in tok or " " in tok:
        return False
    if tok.startswith("<") and tok.endswith(">"):
        return False
    return bool(NOME_RE.match(tok))


def extrair_citados(markdown):
    achados = set()

    def add(bruto):
        if not bruto:
            return
        tok = bruto.strip()
        if not eh_nome_de_campo(tok):
            return
        achados.add(tok)
        ultimo = tok.split(".")[-1]
        if eh_nome_de_campo(ultimo):
            achados.add(ultimo)

    for m in re.finditer(r"`([^`\n]{2,60})`", markdown):
        add(m.group(1))

    for linha in markdown.split("\n"):
        l = linha.strip()
        if not l.startswith("|"):
            continue
        if re.match(r"^\|[\s|:-]+\|?$", l):
            continue
        partes = l.split("|")
        if len(partes) > 1:
            add(re.sub(r"[`*_]", "", partes[1]))

    for m in re.finditer(r'"([A-Za-z_][A-Za-z0-9_]{1,59})"\s*:', markdown):
        add(m.group(1))

    return sorted(achados)


def coletar_campos_da_fonte(spec):
    """Tudo que o spec declara e que um rascunho cita legitimamente.

    Caso real (HubSpot): 10 de 11 suspeitos eram host de `servers`, esquema e
    escopo OAuth de `securitySchemes` e a chave `default` de `responses`. O
    verificador so varria `properties` e parametros, entao acusava identificador
    legitimo da propria fonte. Falso suspeito custa uma rodada de prova manual.
    """
    nomes = set()

    def walk(n, prof=0):
        if prof > 14 or not isinstance(n, (dict, list)):
            return
        if isinstance(n, list):
            for x in n:
                walk(x, prof + 1)
            return
        props = n.get("properties")
        if isinstance(props, dict):
            nomes.update(props.keys())
        # parametros tambem sao campos citaveis (e $ref de parametro ja
        # derefado nao pode virar falso "campo inventado")
        if n.get("name") and n.get("in"):
            nomes.add(n["name"])
        # chaves de resposta ("200", "default") sao citaveis na tabela de status
        if isinstance(n.get("responses"), dict):
            nomes.update(str(k) for k in n["responses"])
        # servers: a URL e o host aparecem em Autenticacao e Endpoint
        if isinstance(n.get("servers"), list):
            for s in n["servers"]:
                url = (s or {}).get("url") or ""
                if url:
                    nomes.add(url)
                    host = re.sub(r"^https?://", "", url).split("/")[0]
                    if host:
                        nomes.add(host)
        for v in n.values():
            walk(v, prof + 1)

    walk(spec)

    # securitySchemes: nome do esquema, chave de apiKey e escopos OAuth
    comp = spec.get("components") or {}
    schemes = comp.get("securitySchemes") or spec.get("securityDefinitions") or {}
    for nome_esquema, esquema in schemes.items():
        nomes.add(nome_esquema)
        if isinstance(esquema, dict):
            if esquema.get("name"):
                nomes.add(esquema["name"])
            if esquema.get("scheme"):
                nomes.add(esquema["scheme"])
            flows = esquema.get("flows") or {}
            for flow in flows.values() if isinstance(flows, dict) else []:
                for escopo in (flow or {}).get("scopes") or {}:
                    nomes.add(escopo)
            for escopo in esquema.get("scopes") or {}:  # swagger 2.0
                nomes.add(escopo)

    # fragmento final de identificador pontuado permitido tambem e permitido
    # (o extrator de citacoes registra "read" ao ver "crm.objects.contacts.read")
    for n in list(nomes):
        if "." in n:
            nomes.add(n.split(".")[-1])
    return nomes


def verificar(markdown, spec, liberar=None):
    permitidos = coletar_campos_da_fonte(spec) | set(liberar or [])
    citados = extrair_citados(markdown)
    ok, suspeitos, considerados = [], [], []

    for c in citados:
        ultimo = c.split(".")[-1]
        if c in permitidos or ultimo in permitidos:
            ok.append(c)
            considerados.append(c)
            continue
        if c.lower() in RUIDO:
            continue
        suspeitos.append(c)
        considerados.append(c)

    total = len(considerados)
    confiavel = total >= 5
    if not confiavel:
        veredito = "INCONCLUSIVO"
    elif suspeitos:
        veredito = "SUSPEITOS"
    else:
        veredito = "OK"

    return {
        "veredito": veredito,
        "total_conferidos": total,
        "ok": sorted(set(ok)),
        "suspeitos": sorted(set(suspeitos)),
        "confiavel": confiavel,
        "aviso": (None if confiavel else
                  "Menos de 5 campos conferidos: NAO leia como aprovacao. Ou o rascunho "
                  "cita pouco campo, ou a extracao de citacoes falhou."),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rascunho", help="arquivo markdown do rascunho")
    ap.add_argument("spec", help="arquivo do spec (json/yaml) ou URL")
    ap.add_argument("--liberar", default="", help="campos legitimos fora do spec, separados por virgula")
    args = ap.parse_args()

    with open(args.rascunho, "r", encoding="utf-8", errors="replace") as f:
        markdown = f.read()
    spec = carregar(args.spec)
    liberar = [x.strip() for x in args.liberar.split(",") if x.strip()]
    print(json.dumps(verificar(markdown, spec, liberar), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
