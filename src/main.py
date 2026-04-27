from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import sqlite3

app = FastAPI(title="API de Tarefas")

def conectar_banco():
    conn = sqlite3.connect("tarefas.db")
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabela():
    conn = conectar_banco()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            feito INTEGER DEFAULT 0,
            prioridade TEXT DEFAULT 'media',
            criado_em TEXT
        )
    """)
    conn.commit()
    conn.close()

criar_tabela()

class Tarefa(BaseModel):
    titulo: str
    prioridade: Optional[str] = "media"

@app.post("/tarefas", status_code=201)
def criar_tarefa(tarefa: Tarefa):
    if tarefa.prioridade not in ["baixa", "media", "alta"]:
        raise HTTPException(status_code=400, detail="Prioridade deve ser baixa, media ou alta")

    conn = conectar_banco()
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = conn.execute(
        "INSERT INTO tarefas (titulo, feito, prioridade, criado_em) VALUES (?, ?, ?, ?)",
        (tarefa.titulo, 0, tarefa.prioridade, agora)
    )
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()

    return {
        "id": id_novo,
        "titulo": tarefa.titulo,
        "feito": False,
        "prioridade": tarefa.prioridade,
        "criado_em": agora
    }

@app.get("/tarefas")
def listar_tarefas(ordem: Optional[str] = None):
    conn = conectar_banco()
    if ordem == "recente":
        rows = conn.execute("SELECT * FROM tarefas ORDER BY criado_em DESC").fetchall()
    elif ordem == "antiga":
        rows = conn.execute("SELECT * FROM tarefas ORDER BY criado_em ASC").fetchall()
    else:
        rows = conn.execute("SELECT * FROM tarefas").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: Tarefa):
    if tarefa.prioridade not in ["baixa", "media", "alta"]:
        raise HTTPException(status_code=400, detail="Prioridade deve ser baixa, media ou alta")

    conn = conectar_banco()
    cursor = conn.execute(
        "UPDATE tarefas SET titulo = ?, prioridade = ? WHERE id = ?",
        (tarefa.titulo, tarefa.prioridade, id)
    )
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"mensagem": "Tarefa atualizada com sucesso"}

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int):
    conn = conectar_banco()
    cursor = conn.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"mensagem": "Tarefa deletada com sucesso"}

@app.patch("/tarefas/{id}/concluir")
def concluir_tarefa(id: int):
    conn = conectar_banco()
    cursor = conn.execute("UPDATE tarefas SET feito = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"mensagem": "Tarefa marcada como concluída"}