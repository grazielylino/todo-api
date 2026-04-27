# Todo API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI.

## Tecnologias utilizadas

- Python 3.14
- FastAPI
- SQLite
- Uvicorn

## Como instalar e rodar localmente

**1. Clone o repositório**

git clone https://github.com/grazielylino/todo-api.git
cd todo-api

**2. Crie e ative o ambiente virtual**

python -m venv venv
venv\Scripts\activate

**3. Instale as dependências**

pip install -r requirements.txt

**4. Rode a aplicação**

uvicorn src.main:app --reload

A API estará disponível em: http://127.0.0.1:8000

A documentação interativa estará em: http://127.0.0.1:8000/docs

## Funcionalidades

- Criar tarefas com título e prioridade
- Listar tarefas com ordenação por data
- Atualizar tarefas
- Marcar tarefas como concluídas
- Deletar tarefas
- Validação de dados automática
- Persistência em banco de dados SQLite