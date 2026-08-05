#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai operacoes de um spec OpenAPI/Swagger com deref e achatamento.

Porta fiel do motor do doc-api (hpx-doc-api-mcp). Cada regra estranha aqui
paga um bug que JA chegou em pagina publicada:
 - allOf e COMPOSICAO (soma), nao alternativa. Tratar como variante devolvia
   ZERO campos em silencio (caso Bling, 41% das operacoes com corpo).
 - Corpo em LISTA: os campos moram em items. Sem isso, toda operacao em lote
   devolvia zero campos (10 dos 44 POSTs do Catalog VTEX).
 - Swagger 2.0 poe o corpo em parameters[in=body], nao em requestBody.
 - Zero campo NUNCA e resposta calada: sai bodyFormato + AVISO.

Uso:
  python extrair.py spec.json --list
  python extrair.py spec.json --tags
  python extrair.py spec.json --path /contas/receber --method post
  python extrair.py https://exemplo.com/openapi.json --list   (se houver rede)

Saida sempre em JSON no stdout.
"""
import argparse
import json
import sys
import urllib.request

MAX_PROF = 12


def carregar(fonte):
    if fonte.startswith("http://") or fonte.startswith("https://"):
        req = urllib.request.Request(fonte, headers={"User-Agent": "doc-api-skill"})
        with urllib.request.urlopen(req, timeout=30) as r:
            texto = r.read().decode("utf-8", errors="replace")
    else:
        with open(fonte, "r", encoding="utf-8", errors="replace") as f:
            texto = f.read()
    texto = texto.strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        try:
            import yaml  # metade dos specs publicados e YAML
            return yaml.safe_load(texto)
        except Exception:
            raise SystemExit(
                "ERRO: o conteudo nao e JSON nem YAML de spec. Se for YAML, "
                "instale pyyaml (pip install pyyaml) e rode de novo."
            )


def deref(node, root, prof=0, seen=None):
    if seen is None:
        seen = frozenset()
    if prof > MAX_PROF or not isinstance(node, (dict, list)):
        return node
    if isinstance(node, list):
        return [deref(n, root, prof + 1, seen) for n in node]
    ref = node.get("$ref")
    if isinstance(ref, str):
        if ref.startswith("#/"):
            if ref in seen:
                return {"note": f"ref ciclico {ref}"}
            alvo = root
            for parte in ref[2:].split("/"):
                parte = parte.replace("~1", "/").replace("~0", "~")
                alvo = alvo.get(parte) if isinstance(alvo, dict) else None
            return deref(alvo, root, prof + 1, seen | {ref})
        return node
    return {k: deref(v, root, prof + 1, seen) for k, v in node.items()}


METODOS = ["get", "post", "put", "patch", "delete"]


def listar_operacoes(spec):
    out = []
    for p, item in (spec.get("paths") or {}).items():
        if not isinstance(item, dict):
            continue
        for m in item:
            if m not in METODOS:
                continue
            op = item[m] or {}
            out.append({
                "path": p,
                "method": m.upper(),
                "summary": op.get("summary") or "",
                "tag": (op.get("tags") or [""])[0],
            })
    return out


def obrigatorios_do(schema, prof=0):
    if not isinstance(schema, dict) or prof > 8:
        return []
    partes = schema.get("allOf") or schema.get("anyOf") or schema.get("oneOf") or []
    out = list(schema.get("required") or [])
    for p in partes:
        out.extend(obrigatorios_do(p, prof + 1))
    return out


def achatar_schema(schema):
    """Achata um schema numa lista de campos de topo (allOf soma, items entra)."""
    vistos = {}

    def coletar(s, prof):
        if not isinstance(s, dict) or prof > 8:
            return
        if s.get("items"):
            coletar(s["items"], prof + 1)
        for parte in s.get("allOf") or []:
            coletar(parte, prof + 1)
        for parte in (s.get("anyOf") or s.get("oneOf") or []):
            coletar(parte, prof + 1)
        req = set(s.get("required") or [])
        for nome, definicao in (s.get("properties") or {}).items():
            if nome in vistos or not isinstance(definicao, dict):
                continue
            vistos[nome] = {
                "name": nome,
                "type": definicao.get("type") or ("object" if definicao.get("properties") else "string"),
                "required": nome in req,
                "deprecated": bool(definicao.get("deprecated")),
                "description": (definicao.get("description") or "").strip(),
                **({"enum": definicao["enum"]} if definicao.get("enum") else {}),
            }
        return

    coletar(schema or {}, 0)
    # obrigatorio declarado numa parte do allOf vale mesmo que o campo tenha
    # sido visto primeiro noutra parte
    for nome in set(obrigatorios_do(schema or {})):
        if nome in vistos:
            vistos[nome]["required"] = True
    return list(vistos.values())


def get_operation(spec, path, method):
    m = method.lower()
    op = ((spec.get("paths") or {}).get(path) or {}).get(m)
    if not op:
        raise SystemExit(f"ERRO: operacao {method.upper()} {path} nao encontrada no spec")
    full = deref(op, spec)

    body = (full.get("requestBody") or {}).get("content")
    body_fields, body_example, body_obrig = [], None, []
    if body:
        ct = body.get("application/json") or next(iter(body.values()), {})
        schema = (ct or {}).get("schema")
        body_example = (ct or {}).get("example") or (ct or {}).get("examples")
        body_fields = achatar_schema(schema)
        body_obrig = list(dict.fromkeys(obrigatorios_do(schema or {})))
    else:
        # Swagger 2.0
        body_param = next((p for p in full.get("parameters") or [] if isinstance(p, dict) and p.get("in") == "body"), None)
        schema = (body_param or {}).get("schema")
        if schema:
            body_fields = achatar_schema(schema)
            body_obrig = list(dict.fromkeys(schema.get("required") or []))
            body_example = schema.get("example")

    responses = {}
    for code, r in (full.get("responses") or {}).items():
        rc = (r or {}).get("content") if isinstance(r, dict) else None
        first = next(iter(rc.values()), None) if rc else None
        ex = None
        if rc:
            ex = (rc.get("application/json") or {}).get("example") or (first or {}).get("example")
        responses[code] = {"description": (r or {}).get("description") or "", "example": ex}

    tem_corpo = bool(body) or any(isinstance(p, dict) and p.get("in") == "body" for p in full.get("parameters") or [])
    if body:
        esquema = (body.get("application/json") or next(iter(body.values()), {}) or {}).get("schema") or {}
    else:
        esquema = ((next((p for p in full.get("parameters") or [] if isinstance(p, dict) and p.get("in") == "body"), None) or {}).get("schema")) or {}
    eh_lista = esquema.get("type") == "array" or bool(esquema.get("items"))

    aviso = None
    if not tem_corpo:
        body_formato = "sem corpo"
    elif body_fields:
        body_formato = "lista de objetos" if eh_lista else "objeto"
    elif eh_lista:
        body_formato = f"lista de {(esquema.get('items') or {}).get('type') or 'valores'}"
        aviso = ("O corpo e uma lista de valores simples, nao de objetos: nao ha tabela de "
                 "campos a montar. Documente o formato da lista, e NAO invente campos.")
    else:
        body_formato = "nao reconhecido"
        aviso = ("Nao consegui extrair os campos deste corpo. NAO escreva campos de memoria "
                 "nem da pagina de documentacao: avise a pessoa que a extracao falhou aqui.")

    out = {
        "path": path,
        "method": method.upper(),
        "summary": full.get("summary") or "",
        "description": full.get("description") or "",
        "servers": spec.get("servers") or full.get("servers"),
        "versaoSpec": spec.get("openapi") or spec.get("swagger") or "",
        "bodyFormato": body_formato,
        "parameters": [
            {"name": p.get("name"), "in": p.get("in"), "required": bool(p.get("required")),
             "description": p.get("description") or ""}
            for p in full.get("parameters") or []
            if isinstance(p, dict) and p.get("in") != "body"
        ],
        "bodyRequired": ([n for n in body_obrig if any(c["name"] == n for c in body_fields)]
                         if body_fields else body_obrig),
        "bodyFields": body_fields,
        "bodyExample": body_example,
        "responses": responses,
    }
    if aviso:
        out["AVISO"] = aviso
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fonte", help="arquivo do spec (json/yaml) ou URL")
    ap.add_argument("--list", action="store_true", help="lista as operacoes")
    ap.add_argument("--tags", action="store_true", help="lista as tags com contagem")
    ap.add_argument("--path", help="path da operacao, ex: /contas/receber")
    ap.add_argument("--method", help="metodo HTTP, ex: post")
    args = ap.parse_args()

    spec = carregar(args.fonte)
    if args.tags:
        contagem = {}
        for o in listar_operacoes(spec):
            contagem[o["tag"] or "(sem tag)"] = contagem.get(o["tag"] or "(sem tag)", 0) + 1
        print(json.dumps(contagem, ensure_ascii=False, indent=2))
    elif args.list:
        print(json.dumps(listar_operacoes(spec), ensure_ascii=False, indent=2))
    elif args.path and args.method:
        print(json.dumps(get_operation(spec, args.path, args.method), ensure_ascii=False, indent=2))
    else:
        ap.error("use --list, --tags, ou --path + --method")


if __name__ == "__main__":
    main()
