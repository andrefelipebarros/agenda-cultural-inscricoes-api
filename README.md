# Inscrições API

API secundária do MVP Agenda Cultural.

O serviço é responsável pelo cadastro e gerenciamento de participantes vinculados aos eventos da API principal.

## Tecnologias

- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite
- Docker

## Rotas

| Método | Rota | Função |
|---|---|---|
| POST | `/inscricoes` | Criar inscrição |
| GET | `/inscricoes` | Listar inscrições |
| GET | `/inscricoes/evento/{evento_id}` | Listar inscrições de um evento |
| GET | `/inscricoes/{inscricao_id}` | Consultar inscrição |
| PUT | `/inscricoes/{inscricao_id}` | Atualizar inscrição |
| DELETE | `/inscricoes/{inscricao_id}` | Excluir inscrição |
| GET | `/health` | Verificar funcionamento |

## Execução com Docker

```bash
docker build -t inscricoes-api .
docker run --rm -p 8001:8001 -v "${PWD}/data:/app/data" inscricoes-api
```

Swagger:

```text
http://localhost:8001/docs
```

## Execução local

Crie o ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente.

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute:

```bash
uvicorn app.main:app --reload --port 8001
```

## Exemplo de inscrição

```json
{
  "evento_id": 1,
  "nome": "Marina Souza",
  "email": "marina@email.com",
  "telefone": "21999999999",
  "confirmada": true
}
```

## Persistência

As inscrições são armazenadas em SQLite no arquivo `data/inscricoes.db`.

Existe uma restrição para impedir que o mesmo e-mail seja cadastrado duas vezes no mesmo evento.
