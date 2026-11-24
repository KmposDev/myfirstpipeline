import pytest
from fastapi.testclient import TestClient

from app.main import create_app, normalize_title


# Prueba unitaria: normalización de títulos
def test_normalize_title():
    assert normalize_title("  Nueva tarea  ") == "Nueva tarea"

    with pytest.raises(ValueError):
        normalize_title("   ")


# Prueba de integración: creación y consulta
def test_create_and_list_tasks():
    client = TestClient(create_app())

    response = client.post(
        "/tasks",
        json={"title": "Aprender Docker"},
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Prueba funcional: completar una tarea
def test_complete_task():
    client = TestClient(create_app())

    client.post("/tasks", json={"title": "Preparar CI"})
    response = client.patch("/tasks/1")

    assert response.status_code == 200
    assert response.json()["completed"] is True


# Prueba funcional: recurso inexistente
def test_task_not_found():
    client = TestClient(create_app())

    response = client.patch("/tasks/999")

    assert response.status_code == 404


# Prueba funcional: validación de datos
def test_invalid_task():
    client = TestClient(create_app())

    response = client.post(
        "/tasks",
        json={"title": ""},
    )

    assert response.status_code == 422


# Prueba del estado del servicio
def test_health():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
