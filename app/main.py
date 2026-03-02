from fastapi import FastAPI

from app.routers import health, todos


app = FastAPI(
    title="Todo List API",
    description=(
        "Простое API для управления задачами (Todo list) "
        "с возможностью добавления, редактирования, удаления задач, "
    ),
    version="1.0.0",
)


app.include_router(health.router)
app.include_router(todos.router)

