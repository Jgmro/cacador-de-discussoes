#!/usr/bin/env python3
"""
Caçador de Discussões 🎯
Encontra GitHub Discussions sem resposta aceita, prontas para você ajudar.

Uso:
    export GITHUB_TOKEN=seu_token_aqui
    python3 cacador.py                      # busca com os termos padrão (pt-BR)
    python3 cacador.py "erro instalar"      # busca com termo customizado
"""

import os
import sys
import requests
from datetime import datetime, timedelta

API_URL = "https://api.github.com/graphql"

# Termos que costumam aparecer em perguntas escritas em português
TERMOS_PADRAO = [
    '"como faço"',
    '"alguém sabe"',
    '"alguém poderia"',
    '"não funciona"',
]

QUERY = """
query($busca: String!, $limite: Int!) {
  search(query: $busca, type: DISCUSSION, first: $limite) {
    discussionCount
    nodes {
      ... on Discussion {
        title
        url
        locked
        createdAt
        comments { totalCount }
        category { name isAnswerable }
        repository {
          nameWithOwner
          stargazerCount
        }
        author { login }
      }
    }
  }
}
"""


def buscar(token: str, termo: str, limite: int = 10) -> list[dict]:
    """Busca discussões sem resposta aceita contendo o termo."""
    
    corte = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    busca = f"{termo} is:unanswered created:>={corte} sort:created-desc"
    resposta = requests.post(
        API_URL,
        json={"query": QUERY, "variables": {"busca": busca, "limite": limite}},
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    resposta.raise_for_status()
    dados = resposta.json()
    if "errors" in dados:
        raise RuntimeError(f"Erro da API: {dados['errors']}")
    return dados["data"]["search"]["nodes"]


def eh_boa_oportunidade(d: dict) -> bool:
    """Filtra: só Q&A (onde existe 'Mark as answer') e não travadas (locked)."""
    if d.get("locked", False):
        return False  # discussão travada: ninguém consegue responder
    return d.get("category", {}).get("isAnswerable", False)


def exibir(discussoes: list[dict]) -> None:
    if not discussoes:
        print("Nenhuma oportunidade encontrada com esses termos. Tente outros!")
        return
    print(f"\n🎯 {len(discussoes)} oportunidade(s) encontrada(s):\n")
    for d in discussoes:
        repo = d["repository"]
        autor = d["author"]["login"] if d["author"] else "(conta removida)"
        print(f"  ⭐ {repo['stargazerCount']:>5}  {repo['nameWithOwner']}")
        print(f"     {d['title']}")
        print(f"     por @{autor} em {d['createdAt'][:10]} · "
              f"{d['comments']['totalCount']} comentário(s)")
        print(f"     {d['url']}\n")


def obter_token() -> str:
    """Procura o token: 1º na variável de ambiente, 2º no arquivo .token"""
    token = os.environ.get("SEU_GITHUB_TOKEN", "").strip()
    if token:
        print("(token lido da variável de ambiente)")
        return token
    try:
        token = open(".token", encoding="utf-8-sig").read().strip()
        if token:
            print("(token lido do arquivo .token)")
            return token
    except FileNotFoundError:
        pass
    sys.exit(
        "Token não encontrado. Duas opções:\n"
        "  1) Defina a variável de ambiente GITHUB_TOKEN, ou\n"
        "  2) Crie um arquivo chamado .token nesta pasta contendo só o token.\n"
        "Crie um token em: github.com/settings/tokens"
    )


def main() -> None:
    token = obter_token()

    termos = [" ".join(sys.argv[1:])] if len(sys.argv) > 1 else TERMOS_PADRAO

    todas: dict[str, dict] = {}
    for termo in termos:
        print(f"Buscando: {termo} ...")
        try:
            for d in buscar(token, termo):
                if d and eh_boa_oportunidade(d):
                    todas[d["url"]] = d  # dedup por URL
        except Exception as erro:
            print(f"  (falhou: {erro})")

    # Mais recentes primeiro
    ordenadas = sorted(todas.values(), key=lambda d: d["createdAt"], reverse=True)
    exibir(ordenadas)


if __name__ == "__main__":
    main()