import { useEffect, useState } from "react";

export default function TodoItem({ todo, onToggle, onDelete, onUpdate, pending }) {
  const [isEditing, setIsEditing] = useState(false);
  const [draftTitle, setDraftTitle] = useState(todo.title);

  useEffect(() => {
    if (!isEditing) {
      setDraftTitle(todo.title);
    }
  }, [todo.title, isEditing]);

  function saveEdit(e) {
    if (e) e.preventDefault();
    const cleanTitle = draftTitle.trim();
    if (!cleanTitle) return;
    if (cleanTitle !== todo.title) {
      onUpdate(todo.id, { title: cleanTitle });
    }
    setIsEditing(false);
  }

  function cancelEdit() {
    setDraftTitle(todo.title);
    setIsEditing(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      saveEdit(e);
    } else if (e.key === "Escape") {
      cancelEdit();
    }
  }

  // Format due date indicator
  let dueDateBadge = null;
  if (todo.due_date) {
    const today = new Date().toISOString().split("T")[0];
    const isOverdue = !todo.completed && todo.due_date < today;
    const isDueToday = !todo.completed && todo.due_date === today;

    dueDateBadge = (
      <span
        className={`todo-due-tag ${isOverdue ? "is-overdue" : isDueToday ? "is-today" : ""}`}
        title={`Due: ${todo.due_date}`}
      >
        <span aria-hidden="true">📅</span>
        {isOverdue ? "Overdue: " : isDueToday ? "Today: " : ""}
        {todo.due_date}
      </span>
    );
  }

  const priorityLabels = {
    high: "High",
    medium: "Medium",
    low: "Low",
  };

  return (
    <li
      className={`todo-item${todo.completed ? " is-completed" : ""}${pending ? " is-pending" : ""}`}
    >
      <label className="todo-check-wrap">
        <input
          className="todo-checkbox"
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo)}
          aria-label={`${todo.completed ? "Mark" : "Complete"} ${todo.title}`}
          disabled={pending}
        />
        <span className="custom-check" aria-hidden="true">✓</span>
      </label>

      <div className="todo-content">
        {isEditing ? (
          <form className="todo-inline-edit" onSubmit={saveEdit}>
            <input
              type="text"
              className="inline-edit-input"
              value={draftTitle}
              onChange={(e) => setDraftTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              autoFocus
              maxLength={200}
            />
            <button type="submit" className="inline-save-btn" title="Save">✓</button>
            <button type="button" className="inline-cancel-btn" onClick={cancelEdit} title="Cancel">✕</button>
          </form>
        ) : (
          <>
            <span className="todo-title" onDoubleClick={() => setIsEditing(true)}>
              {todo.title}
            </span>
            <div className="todo-badges">
              {todo.category && (
                <span className="todo-category-tag">{todo.category}</span>
              )}
              {todo.priority && (
                <span className={`todo-priority-tag priority-${todo.priority}`}>
                  {priorityLabels[todo.priority] || todo.priority}
                </span>
              )}
              {dueDateBadge}
            </div>
          </>
        )}
      </div>

      <div className="todo-actions">
        {!isEditing && (
          <button
            className="edit-button"
            type="button"
            onClick={() => setIsEditing(true)}
            aria-label={`Edit ${todo.title}`}
            title="Edit task title"
            disabled={pending}
          >
            <svg viewBox="0 0 20 20" aria-hidden="true">
              <path d="m13.8 3.2 3 3-9.5 9.5H4.3v-3l9.5-9.5Zm1.8 1.8-.8-.8-1.5 1.5.8.8 1.5-1.5Z" />
            </svg>
          </button>
        )}
        <button
          className="delete-button"
          type="button"
          onClick={() => onDelete(todo.id)}
          aria-label={`Delete ${todo.title}`}
          title="Delete task"
          disabled={pending}
        >
          <svg viewBox="0 0 20 20" aria-hidden="true">
            <path d="M4.5 6h11m-9.5 0 .6 9h6.8l.6-9M8 6V4.5h4V6m-3 2v4m2-4v4" />
          </svg>
        </button>
      </div>
    </li>
  );
}
