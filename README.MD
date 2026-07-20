# Caçador de Discussões

Encontre GitHub Discussions **sem resposta aceita**, prontas para você ajudar — com foco em perguntas em português.

Sabe aquela vontade de contribuir com open source respondendo dúvidas, mas a dificuldade é *achar* perguntas abertas que você consegue responder? O Caçador automatiza essa garimpagem: ele busca na API do GitHub discussões recentes, da categoria Q&A (onde existe o botão "Mark as answer"), que ainda não têm resposta aceita, e te entrega uma lista pronta de oportunidades.

## Como funciona

O script consulta a [API GraphQL do GitHub](https://docs.github.com/graphql) e aplica uma série de filtros:

- **Sem resposta aceita** (`is:unanswered`) — só perguntas ainda abertas;
- **Categoria Q&A** — descarta categorias onde não é possível marcar respostas;
- **Não travadas** — discussões `locked` não aceitam novos comentários, então nem aparecem;
- **Recentes** — só discussões criadas nos últimos 60 dias (autores recentes têm muito mais chance de voltar e marcar sua resposta);
- **Termos em português** — por padrão busca expressões como "como faço" e "alguém sabe", típicas de perguntas escritas em pt-BR.

O resultado sai ordenado da mais recente para a mais antiga, com estrelas do repositório, autor, data e link direto.

## Requisitos

- Python 3.10+
- Biblioteca `requests` (`pip install requests`)
- Um token do GitHub (gratuito, instruções abaixo)

## Configuração do token

A API GraphQL exige autenticação. Crie um token em [github.com/settings/tokens](https://github.com/settings/tokens) → *Generate new token (classic)*. **Nenhum scope é necessário** — o script só lê dados públicos.

Depois, escolha **uma** das formas de informar o token:

**Opção 1 — arquivo `.token` (mais simples):** crie um arquivo chamado `.token` na pasta do script contendo apenas o token.

**Opção 2 — variável de ambiente:**

```bash
# Linux/Mac
export GITHUB_TOKEN=seu_token

# Windows (PowerShell)
$env:GITHUB_TOKEN="seu_token"
```

> ⚠️ **Nunca** commite seu token. O `.gitignore` deste projeto já ignora o arquivo `.token`, mas a regra vale para sempre: token é senha.

## Uso

```bash
# Busca com os termos padrão (pt-BR)
python cacador.py

# Busca com termo customizado
python cacador.py "erro ao instalar"
```

Exemplo de saída:

```
(token lido do arquivo .token)
Buscando: "como faço" ...

🎯 12 oportunidade(s) encontrada(s):

  ⭐ 20626  google/adk-python
     dificuldade com testes
     por @dgsecc em 2026-05-07 · 1 comentário(s)
     https://github.com/google/adk-python/discussions/5628
```

## Dicas de caçada

- Prefira discussões **recentes** e com **poucos comentários** — o autor ainda está por perto;
- Cheque se o comentário existente já não resolveu a questão;
- Evite pedidos de suporte de conta (suspensão, 2FA, conta deletada): só o suporte oficial resolve;
- Cuidado com **importações de fóruns antigos** (Disqus etc.): parecem perguntas abertas, mas o autor original nunca vai voltar;
- Responda com capricho: passo a passo claro e testável aumenta muito a chance do ✔️.

## Roadmap

- [x] Janela de dias configurável por argumento (`--dias 30`)
- [x] Filtro de idioma mais preciso
- [x] Detecção de importações de fóruns antigos
- [x] Ignorar discussões já visitadas (histórico local)

## Licença

MIT — use, modifique e cace à vontade.
