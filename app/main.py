from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=100)


def normalize_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise ValueError("El título no puede estar vacío")
    return title


def create_app() -> FastAPI:
    app = FastAPI(title="TaskFlow API")

    tasks = {}
    next_id = 1

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/tasks")
    def list_tasks():
        return list(tasks.values())

    @app.post("/tasks", status_code=201)
    def create_task(data: TaskInput):
        nonlocal next_id

        try:
            title = normalize_title(data.title)
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from error

        task = {
            "id": next_id,
            "title": title,
            "completed": False,
        }

        tasks[next_id] = task
        next_id += 1
        return task

    @app.patch("/tasks/{task_id}")
    def complete_task(task_id: int):
        if task_id not in tasks:
            raise HTTPException(
                status_code=404,
                detail="Tarea no encontrada",
            )

        tasks[task_id]["completed"] = True
        return tasks[task_id]

    return app


app = create_app()
