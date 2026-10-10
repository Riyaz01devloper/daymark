
import { useEffect, useState } from "react";
import { apiRequest, ApiError } from "./api/client.js";
import AuthForm from "./components/AuthForm.jsx";
import GradeSetup from "./components/GradeSetup.jsx";
import PreviousYearPapers from "./components/PreviousYearPapers.jsx";
import TodoItem from "./components/TodoItem.jsx";

const filters = [
  { id: "all", label: "All tasks" },
  { id: "active", label: "In progress" },
  { id: "completed", label: "Completed" },
];

const studySubjects = [
  "General",
  "Math",
  "Science",
  "English",
  "History",
  "Coding",
];

const defaultCategories = ["General", "Homework", "Exam", "Reading", "Project"];

export default function App() {
  const [user, setUser] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);
  const [todos, setTodos] = useState([]);
  const [summary, setSummary] = useState({ total: 0, active: 0, completed: 0 });
  const [categoriesList, setCategoriesList] = useState([]);

  // Form states
  const [title, setTitle] = useState("");
  const [priority, setPriority] = useState("medium");
  const [dueDate, setDueDate] = useState("");
  const [category, setCategory] = useState("General");
  const [showAdvancedAdd, setShowAdvancedAdd] = useState(false);

  // Filter & Search states
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [filter, setFilter] = useState("all");
  const [categoryFilter, setCategoryFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [page, setPage] = useState(0);
  const [refresh, setRefresh] = useState(0);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  // AI Study tip states
  const [selectedSubject, setSelectedSubject] = useState("General");
  const [studyTip, setStudyTip] = useState("");
  const [studyTipError, setStudyTipError] = useState("");
  const [studyTipLoading, setStudyTipLoading] = useState(false);

  // Grade states
  const [gradeDraft, setGradeDraft] = useState("");
  const [gradeSaving, setGradeSaving] = useState(false);
  const [pendingIds, setPendingIds] = useState([]);

  // Theme state
  const [darkMode, setDarkMode] = useState(() => {
    return localStorage.getItem("daymark_theme") === "dark";
  });

  // Language state (en | hi)
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem("daymark_lang") || "en";
  });

  // Account Settings Modal (Change PIN)
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [currentPin, setCurrentPin] = useState("");
  const [newPin, setNewPin] = useState("");
  const [pinError, setPinError] = useState("");
  const [pinSuccess, setPinSuccess] = useState("");
  const [pinLoading, setPinLoading] = useState(false);

  const pageSize = 25;

  // Apply dark mode class
  useEffect(() => {
    document.documentElement.classList.toggle("dark-theme", darkMode);
    localStorage.setItem("daymark_theme", darkMode ? "dark" : "light");
  }, [darkMode]);

  // Language change handler
  async function handleLanguageChange(newLang) {
    setLanguage(newLang);
    localStorage.setItem("daymark_lang", newLang);
    if (user) {
      try {
        const updatedUser = await apiRequest("/auth/profile", {
          method: "PATCH",
          body: JSON.stringify({ language: newLang }),
        });
        setUser(updatedUser);
      } catch (err) {
        console.error("Failed to update language preference:", err);
      }
    }
  }

  // Restore session
  useEffect(() => {
    let active = true;
    apiRequest("/auth/me")
      .then((currentUser) => {
        if (active) {
          setUser(currentUser);
          if (currentUser?.language) {
            setLanguage(currentUser.language);
            localStorage.setItem("daymark_lang", currentUser.language);
          }
        }
      })
      .catch((requestError) => {
        if (active && !(requestError instanceof ApiError && requestError.status === 401)) {
          setError(`Could not restore your session: ${requestError.message}`);
        }
      })
      .finally(() => {
        if (active) setCheckingSession(false);
      });
    return () => {
      active = false;
    };
  }, []);

  // Debounced search
  useEffect(() => {
    const timeout = window.setTimeout(() => setSearch(searchInput.trim()), 250);
    return () => window.clearTimeout(timeout);
  }, [searchInput]);

  // Load categories
  useEffect(() => {
    if (!user) return;
    apiRequest("/todos/categories")
      .then((cats) => {
        if (Array.isArray(cats)) {
          const combined = Array.from(new Set([...defaultCategories, ...cats]));
          setCategoriesList(combined);
        }
      })
      .catch(() => {});
  }, [user, refresh]);

  // Load todos
  useEffect(() => {
    if (!user) {
      setTodos([]);
      return undefined;
    }

    let active = true;
    const controller = new AbortController();
    const query = new URLSearchParams({
      status: filter,
      search: search.trim(),
      category: categoryFilter,
      priority: priorityFilter,
      limit: String(pageSize),
      offset: String(page * pageSize),
    });

    setLoading(true);
    setError("");

    Promise.all([
      apiRequest(`/todos?${query}`, { signal: controller.signal }),
      apiRequest(`/todos/summary?${new URLSearchParams({ search: search.trim() })}`, {
        signal: controller.signal,
      }),
    ])
      .then(([items, counts]) => {
        if (active) {
          setTodos(items);
          setSummary(counts);
          const filteredTotal = filter === "all" ? counts.total : counts[filter];
          if (items.length === 0 && page > 0 && page * pageSize >= filteredTotal) {
            setPage(Math.max(0, Math.ceil(filteredTotal / pageSize) - 1));
          }
        }
      })
      .catch((requestError) => {
        if (active && requestError.name !== "AbortError") {
          setError(`Could not load tasks: ${requestError.message}`);
        }
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
      controller.abort();
    };
  }, [user, filter, search, categoryFilter, priorityFilter, page, refresh]);

  const activeCount = summary.active;
  const completedCount = summary.completed;

  useEffect(() => {
    setGradeDraft(user?.grade ? String(user.grade) : "");
  }, [user?.grade]);

  async function saveGrade(event) {
    event.preventDefault();
    setGradeSaving(true);
    setStudyTipError("");
    try {
      const updatedUser = await apiRequest("/auth/profile", {
        method: "PATCH",
        body: JSON.stringify({ grade: Number(gradeDraft) }),
      });
      setUser(updatedUser);
      setStudyTip("");
    } catch (requestError) {
      setStudyTipError(`Could not update your class: ${requestError.message}`);
    } finally {
      setGradeSaving(false);
    }
  }

  async function getStudyTip() {
    setStudyTipLoading(true);
    setStudyTipError("");
    try {
      const result = await apiRequest("/suggestions/study-tip", {
        method: "POST",
        body: JSON.stringify({ subject: selectedSubject }),
      });
      setStudyTip(result.tip);
    } catch (requestError) {
      setStudyTipError(requestError.message);
    } finally {
      setStudyTipLoading(false);
    }
  }

  async function addTodo(event) {
    event.preventDefault();
    const cleanTitle = title.trim();
    if (!cleanTitle) {
      setError("Add a task title before saving.");
      return;
    }

    setSaving(true);
    setError("");
    try {
      await apiRequest("/todos", {
        method: "POST",
        body: JSON.stringify({
          title: cleanTitle,
          priority,
          due_date: dueDate || null,
          category: category.trim() || "General",
        }),
      });
      setTitle("");
      setDueDate("");
      setPriority("medium");
      setShowAdvancedAdd(false);
      setPage(0);
      setRefresh((value) => value + 1);
    } catch (requestError) {
      setError(`Could not add task: ${requestError.message}`);
    } finally {
      setSaving(false);
    }
  }

  async function toggleTodo(todo) {
    setPendingIds((ids) => [...ids, todo.id]);
    setError("");
    try {
      const updatedTodo = await apiRequest(`/todos/${todo.id}`, {
        method: "PUT",
        body: JSON.stringify({ completed: !todo.completed }),
      });
      setTodos((currentTodos) =>
        currentTodos.map((item) => (item.id === todo.id ? updatedTodo : item)),
      );
      setRefresh((value) => value + 1);
    } catch (requestError) {
      setError(`Could not update task: ${requestError.message}`);
    } finally {
      setPendingIds((ids) => ids.filter((id) => id !== todo.id));
    }
  }

  async function updateTodo(todoId, patch) {
    setPendingIds((ids) => [...ids, todoId]);
    setError("");
    try {
      const updatedTodo = await apiRequest(`/todos/${todoId}`, {
        method: "PUT",
        body: JSON.stringify(patch),
      });
      setTodos((currentTodos) =>
        currentTodos.map((item) => (item.id === todoId ? updatedTodo : item)),
      );
      setRefresh((value) => value + 1);
    } catch (requestError) {
      setError(`Could not update task: ${requestError.message}`);
    } finally {
      setPendingIds((ids) => ids.filter((id) => id !== todoId));
    }
  }

  async function deleteTodo(todoId) {
    setPendingIds((ids) => [...ids, todoId]);
    setError("");
    try {
      await apiRequest(`/todos/${todoId}`, { method: "DELETE" });
      setTodos((currentTodos) => currentTodos.filter((todo) => todo.id !== todoId));
      setRefresh((value) => value + 1);
    } catch (requestError) {
      setError(`Could not delete task: ${requestError.message}`);
    } finally {
      setPendingIds((ids) => ids.filter((id) => id !== todoId));
    }
  }

  async function handleChangePin(e) {
    e.preventDefault();
    setPinError("");
    setPinSuccess("");
    if (newPin.length !== 6 || !/^\d{6}$/.test(newPin)) {
      setPinError("New PIN must contain exactly 6 digits.");
      return;
    }
    setPinLoading(true);
    try {
      await apiRequest("/auth/password", {
        method: "PATCH",
        body: JSON.stringify({
          current_password: currentPin,
          new_password: newPin,
        }),
      });
      setPinSuccess("6-digit PIN successfully updated!");
      setCurrentPin("");
      setNewPin("");
    } catch (err) {
      setPinError(err.message);
    } finally {
      setPinLoading(false);
    }
  }

  async function signOut() {
    try {
      await apiRequest("/auth/logout", { method: "POST" });
      setUser(null);
      setTodos([]);
      setTitle("");
      setError("");
    } catch (requestError) {
      setError(`Could not sign out: ${requestError.message}`);
    }
  }

  if (checkingSession) {
    return (
      <main className="session-loading">
        <span className="brand-icon" aria-hidden="true">d</span>
        <p>Getting your space ready...</p>
      </main>
    );
  }

  if (!user) {
    return (
      <AuthForm
        onAuthenticated={(loggedInUser) => {
          setError("");
          setUser(loggedInUser);
          if (loggedInUser?.language) {
            setLanguage(loggedInUser.language);
            localStorage.setItem("daymark_lang", loggedInUser.language);
          }
        }}
      />
    );
  }

  if (!user.grade) {
    return (
      <GradeSetup
        user={user}
        onSaved={(savedUser) => {
          setError("");
          setUser(savedUser);
          if (savedUser?.language) {
            setLanguage(savedUser.language);
            localStorage.setItem("daymark_lang", savedUser.language);
          }
        }}
        onSignOut={signOut}
      />
    );
  }

  const hasTasks = todos.length > 0;
  const visibleTaskCount =
    filter === "completed"
      ? completedCount
      : filter === "active"
        ? activeCount
        : summary.total;
  const taskTotalCaption =
    filter === "completed"
      ? "done"
      : filter === "active"
        ? "to go"
        : "in total";

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="daymark home">
          <span className="brand-icon" aria-hidden="true">d</span>
          <span>daymark</span>
        </a>

        <div className="topbar-right">
          {/* Language Switcher */}
          <div className="lang-toggle-group" role="group" aria-label="Language selection">
            <button
              type="button"
              className={`lang-toggle-btn ${language === "en" ? "is-active" : ""}`}
              onClick={() => handleLanguageChange("en")}
              title="Switch to English"
            >
              English
            </button>
            <button
              type="button"
              className={`lang-toggle-btn ${language === "hi" ? "is-active" : ""}`}
              onClick={() => handleLanguageChange("hi")}
              title="हिंदी में बदलें (Switch to Hindi)"
            >
              हिंदी
            </button>
          </div>

          {/* Dark Mode Toggle */}
          <button
            type="button"
            className="theme-toggle-btn"
            onClick={() => setDarkMode(!darkMode)}
            title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
            aria-label="Toggle theme"
          >
            {darkMode ? "☀️ Light" : "🌙 Dark"}
          </button>

          <span className="date-label">
            {new Intl.DateTimeFormat(undefined, {
              weekday: "short",
              month: "short",
              day: "numeric",
            }).format(new Date())}
          </span>
          <span className="topbar-divider" />
          <div className="account-menu">
            <span className="avatar" aria-hidden="true">
              {user.email[0].toUpperCase()}
            </span>
            <span className="account-email">{user.email}</span>
            <button
              type="button"
              className="settings-button"
              onClick={() => {
                setShowSettingsModal(true);
                setPinError("");
                setPinSuccess("");
              }}
              title="Settings & PIN"
            >
              ⚙
            </button>
            <button type="button" className="signout-button" onClick={signOut}>
              Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="dashboard">
        <aside className="side-panel">
          <div className="welcome-block">
            <p className="eyebrow">YOUR PERSONAL SPACE</p>
            <h1>
              Make today <span>count.</span>
            </h1>
            <p>A little progress each day adds up to big results.</p>
          </div>

          {/* AI Study Spark Card */}
          <div className="focus-card study-card">
            <div className="focus-icon" aria-hidden="true">✳</div>
            <p className="focus-title">Study spark for Class {user.grade}</p>

            {/* Subject Selector Chips */}
            <div className="study-subject-chips">
              {studySubjects.map((sub) => (
                <button
                  key={sub}
                  type="button"
                  className={`subject-chip ${selectedSubject === sub ? "is-selected" : ""}`}
                  onClick={() => setSelectedSubject(sub)}
                >
                  {sub}
                </button>
              ))}
            </div>

            <p className="focus-copy" aria-live="polite">
              {studyTip ||
                `Get one practical study tip for ${selectedSubject === "General" ? "your class" : selectedSubject}.`}
            </p>

            <button
              className="study-tip-button"
              type="button"
              onClick={getStudyTip}
              disabled={studyTipLoading}
            >
              {studyTipLoading
                ? "Thinking..."
                : studyTip
                  ? `New ${selectedSubject} tip`
                  : `Get ${selectedSubject} tip`}
            </button>

            {studyTipError && (
              <p className="study-tip-error" role="alert">
                {studyTipError}
              </p>
            )}

            <form className="grade-update-form" onSubmit={saveGrade}>
              <label htmlFor="change-school-grade">Class</label>
              <select
                id="change-school-grade"
                value={gradeDraft}
                onChange={(event) => setGradeDraft(event.target.value)}
                disabled={gradeSaving}
              >
                {Array.from({ length: 12 }, (_, index) => index + 1).map((grade) => (
                  <option key={grade} value={grade}>
                    Class {grade}
                  </option>
                ))}
              </select>
              <button
                type="submit"
                disabled={gradeSaving || Number(gradeDraft) === user.grade}
              >
                {gradeSaving ? "Saving..." : "Update"}
              </button>
            </form>
          </div>

          <div className="side-stats">
            <div className="side-stat">
              <span className="stat-dot stat-dot-green" />
              <span>Still to do</span>
              <strong>{activeCount}</strong>
            </div>
            <div className="side-stat">
              <span className="stat-dot stat-dot-sand" />
              <span>Already done</span>
              <strong>{completedCount}</strong>
            </div>
          </div>
          <p className="side-footer">Made for your day, at your pace.</p>
        </aside>

        <section className="task-workspace" aria-labelledby="tasks-heading">
          <div className="workspace-heading">
            <div>
              <p className="eyebrow">YOUR DAY, YOUR WAY</p>
              <h2 id="tasks-heading">
                Task list<span className="heading-period">.</span>
              </h2>
            </div>
            <span className="task-total">
              {visibleTaskCount} {visibleTaskCount === 1 ? "task" : "tasks"}{" "}
              {taskTotalCaption}
            </span>
          </div>

          {/* Previous Year Questions & Official Resources Section */}
          <PreviousYearPapers
            userGrade={user?.grade || 10}
            language={language}
            onLanguageChange={handleLanguageChange}
          />

          {/* Add Todo Form with Priority & Category */}
          <form className="todo-form-container" onSubmit={addTodo}>
            <div className="todo-main-row">
              <span className="input-plus" aria-hidden="true">+</span>
              <label className="visually-hidden" htmlFor="todo-title">
                Add a new task
              </label>
              <input
                id="todo-title"
                type="text"
                maxLength={200}
                placeholder="What needs to get done?"
                autoComplete="off"
                required
                value={title}
                onChange={(event) => setTitle(event.target.value)}
              />

              <button
                type="button"
                className={`toggle-details-btn ${showAdvancedAdd ? "is-active" : ""}`}
                onClick={() => setShowAdvancedAdd(!showAdvancedAdd)}
                title="Task options (Priority, Category, Due date)"
              >
                ⚙ Options
              </button>

              <button className="primary-button" type="submit" disabled={saving}>
                {saving ? "Adding..." : "Add task"}
                {!saving && <span aria-hidden="true">↗</span>}
              </button>
            </div>

            {showAdvancedAdd && (
              <div className="todo-extra-options">
                <div className="option-field">
                  <label htmlFor="todo-priority">Priority</label>
                  <select
                    id="todo-priority"
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                  >
                    <option value="low">Low Priority</option>
                    <option value="medium">Medium Priority</option>
                    <option value="high">High Priority</option>
                  </select>
                </div>

                <div className="option-field">
                  <label htmlFor="todo-category">Category</label>
                  <input
                    id="todo-category"
                    type="text"
                    list="categories-datalist"
                    placeholder="e.g. Math, Homework"
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    maxLength={50}
                  />
                  <datalist id="categories-datalist">
                    {categoriesList.map((cat) => (
                      <option key={cat} value={cat} />
                    ))}
                  </datalist>
                </div>

                <div className="option-field">
                  <label htmlFor="todo-due-date">Due Date</label>
                  <input
                    id="todo-due-date"
                    type="date"
                    value={dueDate}
                    onChange={(e) => setDueDate(e.target.value)}
                  />
                </div>
              </div>
            )}
          </form>

          {/* Filter and Search Bar */}
          <div className="list-toolbar">
            <div className="filter-tabs" role="tablist" aria-label="Filter tasks">
              {filters.map((item) => (
                <button
                  key={item.id}
                  className={`filter-tab${filter === item.id ? " is-selected" : ""}`}
                  type="button"
                  role="tab"
                  aria-selected={filter === item.id}
                  onClick={() => {
                    setFilter(item.id);
                    setPage(0);
                  }}
                >
                  {item.label}
                  {item.id === "all" && <span>{activeCount + completedCount}</span>}
                </button>
              ))}
            </div>

            <div className="toolbar-filters-right">
              {/* Priority Filter */}
              <select
                className="toolbar-select"
                value={priorityFilter}
                onChange={(e) => {
                  setPriorityFilter(e.target.value);
                  setPage(0);
                }}
                aria-label="Filter by priority"
              >
                <option value="">All Priorities</option>
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
              </select>

              {/* Category Filter */}
              <select
                className="toolbar-select"
                value={categoryFilter}
                onChange={(e) => {
                  setCategoryFilter(e.target.value);
                  setPage(0);
                }}
                aria-label="Filter by category"
              >
                <option value="">All Categories</option>
                {categoriesList.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>

              {/* Search Bar */}
              <label className="search-box">
                <svg viewBox="0 0 20 20" aria-hidden="true">
                  <circle cx="8.7" cy="8.7" r="5.2" />
                  <path d="m12.6 12.6 4 4" />
                </svg>
                <span className="visually-hidden">Search tasks</span>
                <input
                  type="search"
                  placeholder="Search tasks..."
                  value={search}
                  onChange={(event) => {
                    setSearchInput(event.target.value);
                    setPage(0);
                  }}
                />
              </label>
            </div>
          </div>

          {error && (
            <p className="message" role="alert">
              {error}
            </p>
          )}

          {/* Task List */}
          <div className="task-list-wrap">
            {loading ? (
              <p className="empty-state">Loading your tasks...</p>
            ) : hasTasks ? (
              <ul className="todo-list">
                {todos.map((todo) => (
                  <TodoItem
                    key={todo.id}
                    todo={todo}
                    pending={pendingIds.includes(todo.id)}
                    onToggle={toggleTodo}
                    onUpdate={updateTodo}
                    onDelete={deleteTodo}
                  />
                ))}
              </ul>
            ) : (
              <div className="empty-state">
                <span className="empty-illustration" aria-hidden="true">✓</span>
                <h3>
                  {search || filter !== "all" || categoryFilter || priorityFilter
                    ? "No tasks found"
                    : "A fresh page"}
                </h3>
                <p>
                  {search || filter !== "all" || categoryFilter || priorityFilter
                    ? "Try adjusting your search or filters."
                    : "Add your first task above. No rush—start wherever you are."}
                </p>
              </div>
            )}
          </div>

          {visibleTaskCount > pageSize && (
            <nav className="pagination" aria-label="Task list pages">
              <span>
                Showing {page * pageSize + 1}–
                {Math.min((page + 1) * pageSize, visibleTaskCount)} of{" "}
                {visibleTaskCount}
              </span>
              <div>
                <button
                  type="button"
                  disabled={page === 0 || loading}
                  onClick={() =>
                    setPage((currentPage) => Math.max(0, currentPage - 1))
                  }
                >
                  Previous
                </button>
                <button
                  type="button"
                  disabled={(page + 1) * pageSize >= visibleTaskCount || loading}
                  onClick={() => setPage((currentPage) => currentPage + 1)}
                >
                  Next
                </button>
              </div>
            </nav>
          )}

          <footer className="workspace-footer">
            <span>
              <span className="footer-spark" aria-hidden="true">✳</span> One thing at a time.
            </span>
            <span>Your list is saved automatically</span>
          </footer>
        </section>
      </div>

      {/* Settings Modal (Change PIN) */}
      {showSettingsModal && (
        <div
          className="modal-backdrop"
          onClick={() => setShowSettingsModal(false)}
        >
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
            role="dialog"
            aria-modal="true"
            aria-labelledby="settings-heading"
          >
            <div className="modal-header">
              <h3 id="settings-heading">Account Settings</h3>
              <button
                type="button"
                className="modal-close-btn"
                onClick={() => setShowSettingsModal(false)}
                aria-label="Close"
              >
                ✕
              </button>
            </div>

            <div className="modal-body">
              <p className="modal-account-label">
                Signed in as <strong>{user.email}</strong>
              </p>

              <form className="change-pin-form" onSubmit={handleChangePin}>
                <h4>Change 6-digit PIN</h4>
                <label htmlFor="current-pin">Current PIN</label>
                <input
                  id="current-pin"
                  type="password"
                  placeholder="Enter current PIN"
                  maxLength={128}
                  required
                  value={currentPin}
                  onChange={(e) => setCurrentPin(e.target.value)}
                />

                <label htmlFor="new-pin">New 6-Digit PIN</label>
                <input
                  id="new-pin"
                  type="password"
                  inputMode="numeric"
                  pattern="[0-9]{6}"
                  placeholder="Enter new 6-digit PIN"
                  maxLength={6}
                  required
                  value={newPin}
                  onChange={(e) => setNewPin(e.target.value)}
                />

                {pinError && <p className="form-error" role="alert">{pinError}</p>}
                {pinSuccess && <p className="form-success" role="status">{pinSuccess}</p>}

                <button
                  type="submit"
                  className="primary-button pin-save-btn"
                  disabled={pinLoading || !currentPin || newPin.length !== 6}
                >
                  {pinLoading ? "Updating..." : "Update PIN"}
                </button>
              </form>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
