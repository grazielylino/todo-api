from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

app = FastAPI(title="API de Tarefas")

tarefas = []
contador_id = 1

class Tarefa(BaseModel):
    titulo: str
    prioridade: Optional[str] = "media"

class TarefaResposta(BaseModel):
    id: int
    titulo: str
    feito: bool
    prioridade: str
    criado_em: str

@app.post("/tarefas", status_code=201)
def criar_tarefa(tarefa: Tarefa):
    global contador_id

    if tarefa.prioridade not in ["baixa", "media", "alta"]:
        raise HTTPException(status_code=400, detail="Prioridade deve ser baixa, media ou alta")

    nova_tarefa = {
        "id": contador_id,
        "titulo": tarefa.titulo,
        "feito": False,
        "prioridade": tarefa.prioridade,
        "criado_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tarefas.append(nova_tarefa)
    contador_id += 1

    return nova_tarefa

@app.get("/tarefas")
def listar_tarefas(ordem: Optional[str] = None):
    if ordem == "recente":
        return sorted(tarefas, key=lambda x: x["criado_em"], reverse=True)
    if ordem == "antiga":
        return sorted(tarefas, key=lambda x: x["criado_em"])
    return tarefas

@app.put("/tarefas/{id}")
def atualizar_tarefa(id: int, tarefa: Tarefa):
    for t in tarefas:
        if t["id"] == id:
            t["titulo"] = tarefa.titulo
            t["prioridade"] = tarefa.prioridade
            return t
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tarefas/{id}")
def deletar_tarefa(id: int):
    for i, t in enumerate(tarefas):
        if t["id"] == id:
            tarefas.pop(i)
            return {"mensagem": "Tarefa deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")