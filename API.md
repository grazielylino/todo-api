# Documentação da API

Base URL: http://127.0.0.1:8000

---

## POST /tarefas
Cria uma nova tarefa.

**Request:**
{
    "titulo": "Estudar FastAPI",
    "prioridade": "alta"
}

**Prioridades aceitas:** baixa, media, alta

**Response (201):**
{
    "id": 1,
    "titulo": "Estudar FastAPI",
    "feito": false,
    "prioridade": "alta",
    "criado_em": "2026-04-23 16:45:51"
}

**Erros:**
- 400: Prioridade inválida
- 422: Campos obrigatórios ausentes

---

## GET /tarefas
Lista todas as tarefas.

**Parâmetros opcionais:**
- ?ordem=recente — ordena da mais nova para a mais antiga
- ?ordem=antiga — ordena da mais antiga para a mais nova

**Response (200):**
[
    {
        "id": 1,
        "titulo": "Estudar FastAPI",
        "feito": 0,
        "prioridade": "alta",
        "criado_em": "2026-04-23 16:45:51"
    }
]

---

## PUT /tarefas/{id}
Atualiza o título e a prioridade de uma tarefa.

**Request:**
{
    "titulo": "Estudar FastAPI avançado",
    "prioridade": "baixa"
}

**Response (200):**
{
    "mensagem": "Tarefa atualizada com sucesso"
}

**Erros:**
- 400: Prioridade inválida
- 404: Tarefa não encontrada

---

## PATCH /tarefas/{id}/concluir
Marca uma tarefa como concluída.

**Response (200):**
{
    "mensagem": "Tarefa marcada como concluída"
}

**Erros:**
- 404: Tarefa não encontrada

---

## DELETE /tarefas/{id}
Deleta uma tarefa.

**Response (200):**
{
    "mensagem": "Tarefa deletada com sucesso"
}

**Erros:**
- 404: Tarefa não encontrada