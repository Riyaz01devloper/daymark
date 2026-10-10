from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.database import get_connection
from app.schemas import (
    TodoCreate,
    TodoRead,
    TodoStatus,
    TodoSummary,
    TodoUpdate,
    UserRead,
)
from app.security import get_current_user

router = APIRouter()


@router.get("/summary", response_model=TodoSummary)
def summarize_todos(
    user: Annotated[UserRead, Depends(get_current_user)],
    search: Annotated[str, Query(max_length=200)] = "",
) -> TodoSummary:
    query = (
        "SELECT COUNT(*) AS total, "
        "SUM(CASE WHEN completed = 0 THEN 1 ELSE 0 END) AS active, "
        "SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) AS completed "
        "FROM todos WHERE user_id = ?"
    )
    parameters: list[object] = [user.id]
    if search:
        escaped_search = (
            search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        query += " AND title LIKE ? ESCAPE '\\'"
        parameters.append(f"%{escaped_search}%")
    with get_connection() as connection:
        row = connection.execute(query, parameters).fetchone()
    return TodoSummary(
        total=row["total"] or 0,
        active=row["active"] or 0,
        completed=row["completed"] or 0,
    )


@router.get("/categories", response_model=list[str])
def list_categories(
    user: Annotated[UserRead, Depends(get_current_user)],
) -> list[str]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT category FROM todos WHERE user_id = ? AND category IS NOT NULL AND category != '' ORDER BY category",
            (user.id,),
        ).fetchall()
    return [row["category"] for row in rows]



@router.get("", response_model=list[TodoRead])
def list_todos(
    user: Annotated[UserRead, Depends(get_current_user)],
    search: Annotated[str, Query(max_length=200)] = "",
    task_status: Annotated[TodoStatus, Query(alias="status")] = "all",
    category: Annotated[str, Query(max_length=50)] = "",
    priority: Annotated[str, Query(max_length=10)] = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TodoRead]:
    conditions = ["user_id = ?"]
    parameters: list[object] = [user.id]
    if search:
        conditions.append("title LIKE ? ESCAPE '\\'")
        escaped_search = (
            search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        )
        parameters.append(f"%{escaped_search}%")
    if task_status == "active":
        conditions.append("completed = 0")
    elif task_status == "completed":
        conditions.append("completed = 1")
    if category:
        conditions.append("category = ?")
        parameters.append(category)
    if priority and priority in ("low", "medium", "high"):
        conditions.append("priority = ?")
        parameters.append(priority)

    query = (
        "SELECT id, title, completed, created_at, priority, due_date, category FROM todos WHERE "
        + " AND ".join(conditions)
        + " ORDER BY created_at DESC, id DESC LIMIT ? OFFSET ?"
    )
    parameters.extend((limit, offset))

    with get_connection() as connection:
        rows = connection.execute(query, parameters).fetchall()
    return [
        TodoRead(
            id=row["id"],
            title=row["title"],
            completed=bool(row["completed"]),
            created_at=row["created_at"],
            priority=row["priority"] or "medium",
            due_date=row["due_date"],
            category=row["category"] or "General",
        )
        for row in rows
    ]


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: TodoCreate,
    user: Annotated[UserRead, Depends(get_current_user)],
) -> TodoRead:
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO todos (user_id, title, completed, created_at, priority, due_date, category)
            VALUES (?, ?, ?, datetime('now'), ?, ?, ?)
            """,
            (
                user.id,
                todo_data.title,
                1 if todo_data.completed else 0,
                todo_data.priority,
                todo_data.due_date,
                todo_data.category,
            ),
        )
        row = connection.execute(
            "SELECT id, title, completed, created_at, priority, due_date, category FROM todos WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return TodoRead(
        id=row["id"],
        title=row["title"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
        priority=row["priority"] or "medium",
        due_date=row["due_date"],
        category=row["category"] or "General",
    )


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    todo_id: int, user: Annotated[UserRead, Depends(get_current_user)]
) -> TodoRead:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, completed, created_at, priority, due_date, category FROM todos
            WHERE id = ? AND user_id = ?
            """,
            (todo_id, user.id),
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoRead(
        id=row["id"],
        title=row["title"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
        priority=row["priority"] or "medium",
        due_date=row["due_date"],
        category=row["category"] or "General",
    )


@router.put("/{todo_id}", response_model=TodoRead)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    user: Annotated[UserRead, Depends(get_current_user)],
) -> TodoRead:
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT id FROM todos WHERE id = ? AND user_id = ?",
            (todo_id, user.id),
        ).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        updates: list[str] = []
        parameters: list[object] = []
        if todo_data.title is not None:
            updates.append("title = ?")
            parameters.append(todo_data.title)
        if todo_data.completed is not None:
            updates.append("completed = ?")
            parameters.append(1 if todo_data.completed else 0)
        if todo_data.priority is not None:
            updates.append("priority = ?")
            parameters.append(todo_data.priority)
        if todo_data.due_date is not None:
            updates.append("due_date = ?")
            parameters.append(todo_data.due_date if todo_data.due_date else None)
        if todo_data.category is not None:
            updates.append("category = ?")
            parameters.append(todo_data.category)

        if updates:
            parameters.extend([todo_id, user.id])
            connection.execute(
                f"UPDATE todos SET {', '.join(updates)} WHERE id = ? AND user_id = ?",
                parameters,
            )

        row = connection.execute(
            """
            SELECT id, title, completed, created_at, priority, due_date, category FROM todos
            WHERE id = ? AND user_id = ?
            """,
            (todo_id, user.id),
        ).fetchone()

    return TodoRead(
        id=row["id"],
        title=row["title"],
        completed=bool(row["completed"]),
        created_at=row["created_at"],
        priority=row["priority"] or "medium",
        due_date=row["due_date"],
        category=row["category"] or "General",
    )


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int, user: Annotated[UserRead, Depends(get_current_user)]
) -> Response:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user.id)
        )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

