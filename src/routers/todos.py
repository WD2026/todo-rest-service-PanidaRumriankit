import os

from fastapi import APIRouter, HTTPException, Request, Response, Query, status

from ..models import Todo, TodoCreate
from ..persistence import TodoDao

from ..logging_config import get_logger

DATA_FILE = os.getenv("TODO_DATA_FILE", "./data/todo_data.json")

router = APIRouter(prefix="/todos", tags=["Todos"])
dao = TodoDao(DATA_FILE)
logger = get_logger(__name__)

@router.get("/", response_model=list[Todo])
def get_todos():
    """Get all todos."""
    return dao.get_all()


@router.post("/", response_model=Todo, status_code=201)
def create_todo(todo: TodoCreate, request: Request, response: Response):
    """Create and save a new todo. A unique ID is assigned."""
    created = dao.save(todo)
    logger.info("Todo created", todo_id=created.id)
    # Return the location of the new todo.
    location = request.url_for("get_todo", todo_id=created.id).path
    response.headers["Location"] = location
    return created


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    """Get a specific todo by id.

    :param todo_id: identifier of the todo to get.
    """
    todo = dao.get(todo_id)
    if not todo:
        logger.warning("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info("Todo retrieved", todo_id=todo_id)
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):
    """Update an existing Todo.

    :param todo_id: identifier of the todo to update
    :param todo: revised data for the todo
    """
    existing = dao.get(todo_id)
    if not existing:
        logger.warning("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")

    updated = Todo(
        id=todo_id,
        text=todo.text,
        done=todo.done,
    )

    logger.info("Todo updated", todo_id=todo_id)
    return dao.update(updated)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """Delete a Todo.

    :param todo_id: identifier of the todo to delete

    Return 204 (or 200 + message) if todo is deleted.
    Return 404 if todo is not found.
    """
    try:
        dao.delete(todo_id)
        logger.info("Todo deleted", todo_id=todo_id)
    except ValueError:
        logger.warning("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")

@router.options("/", status_code=204)
def todos_options(response: Response):
    """Return the allowed HTTP methods for this URL."""
    response.headers["Allow"] = "GET,POST,OPTIONS"


@router.options("/{todo_id}", status_code=204)
def todo_options(todo_id: int, response: Response):
    """Return the allowed HTTP methods for this URL."""
    todo = dao.get(todo_id)
    if not todo:
        logger.warning("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    response.headers["Allow"] = "GET,PUT,DELETE,OPTIONS"
