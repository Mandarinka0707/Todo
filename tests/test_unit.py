import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime
from app.src import crud
from app.src.main import app
from app.src.models import Todo


client = TestClient(app)


@pytest.fixture
def mock_todo_obj():
    return Todo(
        id=1,
        title="Тестовая задача",
        description="Описание задачи",
        priority=1,
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@patch("app.src.routers.todos.crud.create_todo")
def test_create_todo_unit(mock_create_todo, mock_todo_obj):
    mock_create_todo.return_value = mock_todo_obj

    response = client.post(
        "/api/todos",
        json={"title": "Тестовая задача", "description": "Описание задачи", "priority": 1}
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Тестовая задача"
    assert response.json()["id"] == 1

    mock_create_todo.assert_called_once()


@patch("app.src.routers.todos.crud.get_todo")
def test_get_todo_not_found(mock_get_todo):
    mock_get_todo.return_value = None

    response = client.get("/api/todos/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
    mock_get_todo.assert_called_once()


@patch("app.src.routers.todos.crud.get_todo")
def test_get_todo_success(mock_get_todo, mock_todo_obj):
    mock_get_todo.return_value = mock_todo_obj

    response = client.get("/api/todos/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Тестовая задача"


@patch("app.src.routers.todos.crud.delete_todo")
@patch("app.src.routers.todos.crud.get_todo")
def test_delete_todo_success(mock_get_todo, mock_delete_todo, mock_todo_obj):
    mock_get_todo.return_value = mock_todo_obj

    mock_delete_todo.return_value = None

    response = client.delete("/api/todos/1")

    assert response.status_code == 204
    mock_get_todo.assert_called_once()
    mock_delete_todo.assert_called_once()


def test_crud_delete_todo(mock_todo_obj):

    mock_db = MagicMock()

    crud.delete_todo(mock_db, mock_todo_obj)

    mock_db.delete.assert_called_once_with(mock_todo_obj)
    mock_db.commit.assert_called_once()


def test_crud_create_todo():
    mock_db = MagicMock()
    from app.src.schemas import TodoCreate
    todo_in = TodoCreate(title="Новая", priority=2)

    result = crud.create_todo(mock_db, todo_in)
    assert isinstance(result, Todo)
    assert result.title == "Новая"
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()
