import sqlite3

import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app
from app.routers import suggestions
from app.security import hash_password

TEST_PIN = "123456"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "test-todos.db")
    with TestClient(app) as test_client:
        yield test_client


def register(client: TestClient, email: str = "person@example.com") -> None:
    response = client.post(
        "/auth/register",
        json={"email": email, "password": TEST_PIN},
    )
    assert response.status_code == 201, response.text
    assert "todo_session" not in response.cookies


def test_registration_validation_and_duplicate_email(client: TestClient) -> None:
    assert client.post(
        "/auth/register",
        json={"email": "not-an-email", "password": TEST_PIN},
    ).status_code == 422
    assert client.post(
        "/auth/register",
        json={"email": "person@example.com", "password": "short"},
    ).status_code == 422
    assert client.post(
        "/auth/register",
        json={"email": "person@example.com", "password": "1234567"},
    ).status_code == 422
    assert client.post(
        "/auth/register",
        json={"email": "person@example.com", "password": "12ab56"},
    ).status_code == 422

    register(client)
    assert client.get("/auth/me").status_code == 401
    assert client.post(
        "/auth/register",
        json={"email": "PERSON@example.com", "password": TEST_PIN},
    ).status_code == 409


def test_registration_requires_login_to_access_tasks(client: TestClient) -> None:
    assert client.post(
        "/auth/register",
        json={"email": "new-user@example.com", "password": TEST_PIN},
    ).status_code == 201
    assert client.cookies.get("todo_session") is None
    assert client.get("/auth/me").status_code == 401
    assert client.get("/todos").status_code == 401
    login = client.post(
        "/auth/login",
        json={"email": "new-user@example.com", "password": TEST_PIN},
    )
    assert login.status_code == 200
    assert client.cookies.get("todo_session")
    assert client.get("/auth/me").json()["email"] == "new-user@example.com"
    assert client.post("/auth/logout").status_code == 204
    assert client.get("/auth/me").status_code == 401


def test_todos_require_auth_and_are_isolated_by_account(client: TestClient) -> None:
    assert client.get("/todos").status_code == 401

    first_user = TestClient(app)
    second_user = TestClient(app)
    register(first_user, "first@example.com")
    register(second_user, "second@example.com")
    assert first_user.post(
        "/auth/login",
        json={"email": "first@example.com", "password": TEST_PIN},
    ).status_code == 200
    assert second_user.post(
        "/auth/login",
        json={"email": "second@example.com", "password": TEST_PIN},
    ).status_code == 200

    created = first_user.post("/todos", json={"title": "Private task"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    assert [todo["title"] for todo in first_user.get("/todos").json()] == [
        "Private task"
    ]
    assert second_user.get("/todos").json() == []
    assert second_user.get(f"/todos/{task_id}").status_code == 404
    assert second_user.put(
        f"/todos/{task_id}",
        json={"title": "Not yours", "completed": True},
    ).status_code == 404
    assert second_user.delete(f"/todos/{task_id}").status_code == 404
    assert first_user.get(f"/todos/{task_id}").json()["title"] == "Private task"
    first_user.close()
    second_user.close()


def test_task_validation_filtering_and_pagination(client: TestClient) -> None:
    register(client)
    client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    )
    assert client.post("/todos", json={"title": "   "}).status_code == 422
    assert client.post("/todos", json={"title": "x" * 201}).status_code == 422

    first = client.post("/todos", json={"title": "Plan the week"}).json()
    second = client.post(
        "/todos", json={"title": "Read a book", "completed": True}
    ).json()
    assert len(client.get("/todos?status=active").json()) == 1
    assert len(client.get("/todos?status=completed").json()) == 1
    assert client.get("/todos?search=week").json()[0]["id"] == first["id"]
    assert client.get("/todos?limit=1&offset=1").json()[0]["id"] == first["id"]
    assert client.get("/todos/summary").json() == {
        "total": 2,
        "active": 1,
        "completed": 1,
    }
    assert client.put(
        f"/todos/{first['id']}",
        json={"title": "Plan the week", "completed": True},
    ).json()["completed"] is True
    assert client.delete(f"/todos/{second['id']}").status_code == 204
    assert client.get(f"/todos/{second['id']}").status_code == 404


def test_password_is_hashed_and_login_restores_persisted_todos(client: TestClient):
    register(client)
    with database.get_connection() as connection:
        stored_hash = connection.execute(
            "SELECT password_hash FROM users WHERE email = ?",
            ("person@example.com",),
        ).fetchone()["password_hash"]
    assert stored_hash != TEST_PIN
    assert stored_hash.startswith("scrypt$")

    assert client.post("/todos", json={"title": "Keep me"}).status_code == 401
    client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    )
    client.post("/todos", json={"title": "Keep me"})
    database.initialize_database()
    client.cookies.clear()
    login = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": "wrong-password"},
    )
    assert login.status_code == 401
    assert client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    ).status_code == 200
    assert [todo["title"] for todo in client.get("/todos").json()] == ["Keep me"]

    client.post("/auth/logout")
    assert client.get("/auth/me").status_code == 401


def test_login_is_rate_limited(client: TestClient) -> None:
    register(client)
    for _ in range(10):
        assert client.post(
            "/auth/login",
            json={"email": "person@example.com", "password": "wrong-password"},
        ).status_code == 401
    response = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    )
    assert response.status_code == 429


def test_existing_long_password_can_still_sign_in(client: TestClient) -> None:
    with database.get_connection() as connection:
        connection.execute(
            "INSERT INTO users (email, password_hash, created_at) "
            "VALUES (?, ?, datetime('now'))",
            ("legacy@example.com", hash_password("a-long-test-password")),
        )
    response = client.post(
        "/auth/login",
        json={"email": "legacy@example.com", "password": "a-long-test-password"},
    )
    assert response.status_code == 200


def test_grade_profile_and_short_gemini_study_tip(
    client: TestClient, monkeypatch
) -> None:
    assert client.post("/suggestions/study-tip").status_code == 401
    register(client)
    assert client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    ).status_code == 200
    assert client.get("/auth/me").json()["grade"] is None
    assert client.post("/suggestions/study-tip").status_code == 400

    assert client.patch("/auth/profile", json={"grade": 13}).status_code == 422
    profile = client.patch("/auth/profile", json={"grade": 8})
    assert profile.status_code == 200
    assert profile.json()["grade"] == 8
    assert client.get("/auth/me").json()["grade"] == 8

    request_details = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "candidates": [
                    {"content": {"parts": [{"text": "Review with flashcards."}]}}
                ]
            }

    class FakeClient:
        def __init__(self, timeout: int) -> None:
            request_details["timeout"] = timeout

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, url: str, *, headers: dict, json: dict):
            request_details.update(url=url, headers=headers, body=json)
            return FakeResponse()

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    monkeypatch.setattr(suggestions.httpx, "AsyncClient", FakeClient)
    response = client.post("/suggestions/study-tip")
    assert response.status_code == 200
    assert response.json() == {"tip": "Review with flashcards."}
    assert request_details["timeout"] == 15
    assert request_details["url"].endswith(
        "/gemini-3.5-flash-lite:generateContent"
    )
    assert request_details["headers"]["x-goog-api-key"] == "test-key"
    assert "Class 8" in request_details["body"]["contents"][0]["parts"][0]["text"]
    assert (
        request_details["body"]["generationConfig"]
        == {"maxOutputTokens": 48}
    )


def test_study_tip_requires_gemini_configuration(
    client: TestClient, monkeypatch
) -> None:
    register(client)
    client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    )
    client.patch("/auth/profile", json={"grade": 10})
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    response = client.post("/suggestions/study-tip")
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_each_study_tip_differs_from_the_previous_tip(
    client: TestClient, monkeypatch
) -> None:
    register(client)
    client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": TEST_PIN},
    )
    client.patch("/auth/profile", json={"grade": 10})

    prompts = []
    tips = [
        "Use spaced repetition to review key facts.",
        "Use spaced repetition to review key facts.",
        "Explain a concept aloud without notes.",
    ]

    class FakeResponse:
        def __init__(self, tip: str) -> None:
            self.tip = tip

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"candidates": [{"content": {"parts": [{"text": self.tip}]}}]}

    class FakeClient:
        def __init__(self, timeout: int) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, url: str, *, headers: dict, json: dict):
            prompts.append(json["contents"][0]["parts"][0]["text"])
            return FakeResponse(tips[min(len(prompts) - 1, len(tips) - 1)])

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(suggestions.httpx, "AsyncClient", FakeClient)
    first = client.post("/suggestions/study-tip")
    second = client.post("/suggestions/study-tip")

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["tip"] != second.json()["tip"]
    assert len(prompts) == 3
    assert first.json()["tip"] in prompts[1]
    assert first.json()["tip"] in prompts[2]
    with database.get_connection() as connection:
        saved_tips = connection.execute(
            "SELECT tip FROM study_tips WHERE user_id = 1 ORDER BY id"
        ).fetchall()
    assert [row["tip"] for row in saved_tips] == [
        first.json()["tip"],
        second.json()["tip"],
    ]


def test_existing_database_gets_nullable_grade_column(tmp_path, monkeypatch) -> None:
    path = tmp_path / "legacy-todos.db"
    with sqlite3.connect(path) as connection:
        connection.execute(
            "CREATE TABLE users ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "email TEXT NOT NULL COLLATE NOCASE UNIQUE, "
            "password_hash TEXT NOT NULL, created_at TEXT NOT NULL)"
        )
        connection.execute(
            "INSERT INTO users (email, password_hash, created_at) "
            "VALUES (?, ?, datetime('now'))",
            ("legacy@example.com", hash_password(TEST_PIN)),
        )

    monkeypatch.setattr(database, "DATABASE_PATH", path)
    with TestClient(app) as legacy_client:
        assert legacy_client.post(
            "/auth/login",
            json={"email": "legacy@example.com", "password": TEST_PIN},
        ).status_code == 200
        assert legacy_client.get("/auth/me").json()["grade"] is None


def test_change_password(client: TestClient) -> None:
    register(client, "changepin@example.com")
    client.post(
        "/auth/login",
        json={"email": "changepin@example.com", "password": TEST_PIN},
    )
    # Incorrect current password fails
    bad = client.patch(
        "/auth/password",
        json={"current_password": "999999", "new_password": "654321"},
    )
    assert bad.status_code == 400

    # Invalid new PIN format fails
    invalid = client.patch(
        "/auth/password",
        json={"current_password": TEST_PIN, "new_password": "short"},
    )
    assert invalid.status_code == 422

    # Successful PIN change
    success = client.patch(
        "/auth/password",
        json={"current_password": TEST_PIN, "new_password": "654321"},
    )
    assert success.status_code == 204

    # Sign in with old PIN fails
    client.post("/auth/logout")
    assert client.post(
        "/auth/login",
        json={"email": "changepin@example.com", "password": TEST_PIN},
    ).status_code == 401

    # Sign in with new PIN succeeds
    assert client.post(
        "/auth/login",
        json={"email": "changepin@example.com", "password": "654321"},
    ).status_code == 200


def test_todo_priority_category_and_due_date(client: TestClient) -> None:
    register(client, "metadata@example.com")
    client.post(
        "/auth/login",
        json={"email": "metadata@example.com", "password": TEST_PIN},
    )
    # Create todo with priority, due date, category
    resp = client.post(
        "/todos",
        json={
            "title": "Math assignment",
            "priority": "high",
            "due_date": "2026-10-15",
            "category": "Math",
        },
    )
    assert resp.status_code == 201
    item = resp.json()
    assert item["priority"] == "high"
    assert item["due_date"] == "2026-10-15"
    assert item["category"] == "Math"

    # Categories endpoint
    cats = client.get("/todos/categories").json()
    assert "Math" in cats

    # Filter by category and priority
    assert len(client.get("/todos?category=Math").json()) == 1
    assert len(client.get("/todos?category=Science").json()) == 0
    assert len(client.get("/todos?priority=high").json()) == 1
    assert len(client.get("/todos?priority=low").json()) == 0

    # Partial update (edit title and priority)
    updated = client.put(
        f"/todos/{item['id']}",
        json={"title": "Math Chapter 4", "priority": "medium"},
    ).json()
    assert updated["title"] == "Math Chapter 4"
    assert updated["priority"] == "medium"
    assert updated["category"] == "Math"
    assert updated["due_date"] == "2026-10-15"


def test_subject_study_tip(client: TestClient, monkeypatch) -> None:
    register(client, "subject@example.com")
    client.post(
        "/auth/login",
        json={"email": "subject@example.com", "password": TEST_PIN},
    )
    client.patch("/auth/profile", json={"grade": 9})

    captured_prompt = {}

    class FakeResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {
                "candidates": [
                    {"content": {"parts": [{"text": "Practice 5 equations daily."}]}}
                ]
            }

    class FakeClient:
        def __init__(self, timeout: int) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, url: str, *, headers: dict, json: dict):
            captured_prompt["text"] = json["contents"][0]["parts"][0]["text"]
            return FakeResponse()

    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(suggestions.httpx, "AsyncClient", FakeClient)

    res = client.post("/suggestions/study-tip", json={"subject": "Algebra"})
    assert res.status_code == 200
    assert res.json()["tip"] == "Practice 5 equations daily."
    assert "Algebra" in captured_prompt["text"]


def test_spa_serving_and_health(client: TestClient) -> None:
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json() == {"status": "ok"}

    root = client.get("/")
    assert root.status_code == 200
    assert "text/html" in root.headers.get("content-type", "")
    assert "daymark" in root.text


def test_cors_middleware_headers(client: TestClient) -> None:
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"


def test_todo_regression_security_isolation_and_edge_cases(client: TestClient) -> None:
    # Register two separate users
    user_a = TestClient(app)
    user_b = TestClient(app)
    register(user_a, "user_a@example.com")
    register(user_b, "user_b@example.com")
    user_a.post("/auth/login", json={"email": "user_a@example.com", "password": TEST_PIN})
    user_b.post("/auth/login", json={"email": "user_b@example.com", "password": TEST_PIN})

    # User A creates a task
    created = user_a.post("/todos", json={"title": "User A secret task", "priority": "high", "category": "Confidential"}).json()
    task_id = created["id"]

    # User B cannot read, update, or delete User A's task
    assert user_b.get(f"/todos/{task_id}").status_code == 404
    assert user_b.put(f"/todos/{task_id}", json={"title": "Hacked"}).status_code == 404
    assert user_b.delete(f"/todos/{task_id}").status_code == 404

    # User A cannot update non-existent task
    assert user_a.put("/todos/999999", json={"title": "Ghost"}).status_code == 404
    assert user_a.delete("/todos/999999").status_code == 404

    # Updating with empty title fails validation (422)
    assert user_a.put(f"/todos/{task_id}", json={"title": "   "}).status_code == 422

    # Category defaults to "General" if empty string passed in creation
    general_task = user_a.post("/todos", json={"title": "General Task", "category": ""}).json()
    assert general_task["category"] == "General"

    user_a.close()
    user_b.close()


def test_auth_session_invalidation_regression(client: TestClient) -> None:
    register(client, "session_test@example.com")
    client.post("/auth/login", json={"email": "session_test@example.com", "password": TEST_PIN})
    assert client.get("/auth/me").status_code == 200

    # Logout
    logout = client.post("/auth/logout")
    assert logout.status_code == 204

    # After logout, accessing protected endpoints fails with 401
    assert client.get("/auth/me").status_code == 401
    assert client.get("/todos").status_code == 401


def test_study_official_resources_and_pyqs(client: TestClient) -> None:
    register(client, "student_cbse@example.com")
    client.post("/auth/login", json={"email": "student_cbse@example.com", "password": TEST_PIN})
    client.patch("/auth/profile", json={"grade": 10})

    # Test official resources for default grade (10)
    res = client.get("/study/official-resources")
    assert res.status_code == 200
    data = res.json()
    assert data["class_grade"] == 10
    assert "cbse.gov.in" in data["board_pyq_url"]
    assert "ncert.nic.in" in data["ncert_books_url"]
    assert "cbseacademic.nic.in" in data["sqp_2024_25_url"]

    # Test official resources with explicit grade query (12)
    res12 = client.get("/study/official-resources?class_grade=12")
    assert res12.status_code == 200
    data12 = res12.json()
    assert data12["class_grade"] == 12
    assert "CLASSXII" in data12["sqp_2024_25_url"]

    # Test curriculum
    curriculum_res = client.get("/study/curriculum?class_grade=10")
    assert curriculum_res.status_code == 200
    assert "Science" in curriculum_res.json()["curriculum"]

    # Test PYQs
    pyq_res = client.get("/study/pyqs?class_grade=10&subject=Science")
    assert pyq_res.status_code == 200
    pyqs = pyq_res.json()
    assert len(pyqs) > 0
    assert pyqs[0]["class_grade"] == 10
    assert pyqs[0]["subject"] == "Science"


def test_chapter_resources_notes_and_animation_videos(client: TestClient) -> None:
    # Requires authentication
    unauth = client.get("/study/chapter-resources?class_grade=10&subject=Science")
    assert unauth.status_code == 401

    register(client, "resources_student@example.com")
    client.post(
        "/auth/login",
        json={"email": "resources_student@example.com", "password": TEST_PIN},
    )

    # Class 10 Science chapters
    res10 = client.get("/study/chapter-resources?class_grade=10&subject=Science")
    assert res10.status_code == 200
    chapters10 = res10.json()
    assert len(chapters10) == 13
    first_ch = chapters10[0]
    assert first_ch["class_grade"] == 10
    assert first_ch["subject"] == "Science"
    assert first_ch["chapter"] == "Chemical Reactions and Equations"
    assert "youtube.com" in first_ch["animation_video_url"]
    assert "animated+concept" in first_ch["animation_video_url"]
    assert "diksha.gov.in" in first_ch["diksha_video_url"]
    assert "ncert.nic.in" in first_ch["ncert_book_url"]
    assert len(first_ch["summary_notes"]) > 100
    assert len(first_ch["key_takeaways"]) >= 3

    # Filter specific chapter
    res_filtered = client.get(
        "/study/chapter-resources?class_grade=10&subject=Science&chapter=Electricity"
    )
    assert res_filtered.status_code == 200
    filtered = res_filtered.json()
    assert len(filtered) == 1
    assert filtered[0]["chapter"] == "Electricity"
    assert "Ohm's Law" in filtered[0]["summary_notes"]

    # Class 12 Physics
    res12 = client.get("/study/chapter-resources?class_grade=12&subject=Physics")
    assert res12.status_code == 200
    assert len(res12.json()) == 14

    # Primary Class 1 Mathematics
    res1 = client.get("/study/chapter-resources?class_grade=1&subject=Mathematics")
    assert res1.status_code == 200
    assert len(res1.json()) == 7


def test_language_preference_and_hindi_content(client: TestClient) -> None:
    register(client, "hindi_student@example.com")
    client.post(
        "/auth/login",
        json={"email": "hindi_student@example.com", "password": TEST_PIN},
    )

    # Initial language is English
    me = client.get("/auth/me").json()
    assert me["language"] == "en"

    # Update language preference to Hindi
    updated = client.patch("/auth/profile", json={"language": "hi"})
    assert updated.status_code == 200
    assert updated.json()["language"] == "hi"
    assert client.get("/auth/me").json()["language"] == "hi"

    # Test Hindi Curriculum
    curriculum_hi = client.get("/study/curriculum?class_grade=10&language=hi")
    assert curriculum_hi.status_code == 200
    cur_data = curriculum_hi.json()
    assert cur_data["language"] == "hi"
    assert "विज्ञान" in cur_data["curriculum"]
    assert "गणित" in cur_data["curriculum"]
    assert "रासायनिक अभिक्रियाएँ एवं समीकरण" in cur_data["curriculum"]["विज्ञान"]
    assert "वास्तविक संख्याएँ" in cur_data["curriculum"]["गणित"]

    # Test Hindi Chapter Resources & Accurate Notes
    res_hi = client.get("/study/chapter-resources?class_grade=10&subject=विज्ञान&language=hi")
    assert res_hi.status_code == 200
    chapters = res_hi.json()
    assert len(chapters) == 13

    ch1 = chapters[0]
    assert ch1["chapter"] == "रासायनिक अभिक्रियाएँ एवं समीकरण"
    assert ch1["subject"] == "विज्ञान"
    assert ch1["language"] == "hi"
    # Check textbook-accurate Hindi terminology in notes
    assert "द्रव्यमान संरक्षण" in ch1["summary_notes"]
    assert "संयोजन अभिक्रिया" in ch1["summary_notes"]
    assert "रेडॉक्स" in ch1["summary_notes"]
    # Check Hindi animated video link
    assert "animated+explanation+in+hindi" in ch1["animation_video_url"]
    assert "%E0%A4%95%E0%A4%95%E0%A5%8D%E0%A4%B7%E0%A4%BE" in ch1["animation_video_url"]  # 'कक्षा'

    # Filter specific chapter in Hindi (matches 'विद्युत' and 'विद्युत धारा के चुंबकीय प्रभाव')
    res_ch_filter = client.get(
        "/study/chapter-resources?class_grade=10&subject=विज्ञान&chapter=विद्युत&language=hi"
    )
    assert res_ch_filter.status_code == 200
    filtered_hi = res_ch_filter.json()
    assert len(filtered_hi) == 2
    assert any(c["chapter"] == "विद्युत" and "ओम का नियम" in c["summary_notes"] for c in filtered_hi)

    # Official resources in Hindi
    off_res = client.get("/study/official-resources?class_grade=10&language=hi")
    assert off_res.status_code == 200
    assert "कक्षा 10" in off_res.json()["title"]

    # Revert to English
    client.patch("/auth/profile", json={"language": "en"})
    assert client.get("/auth/me").json()["language"] == "en"
    curriculum_en = client.get("/study/curriculum?class_grade=10&language=en")
    assert "Science" in curriculum_en.json()["curriculum"]


def test_bearer_token_authentication(client: TestClient) -> None:
    # 1. Register and login
    email = "tokenuser@example.com"
    client.post("/auth/register", json={"email": email, "password": TEST_PIN})
    login_res = client.post("/auth/login", json={"email": email, "password": TEST_PIN})
    assert login_res.status_code == 200
    token = login_res.json().get("token")
    assert token is not None and len(token) > 20

    # 2. Clear client cookies to simulate Android WebView with no cookies
    client.cookies.clear()
    assert client.get("/auth/me").status_code == 401

    # 3. Use Authorization: Bearer <token> header
    headers = {"Authorization": f"Bearer {token}"}
    me_res = client.get("/auth/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

    # 4. Patch profile with Bearer token (what GradeSetup does)
    profile_res = client.patch("/auth/profile", json={"grade": 10}, headers=headers)
    assert profile_res.status_code == 200
    assert profile_res.json()["grade"] == 10

    # 5. Create todo with Bearer token
    todo_res = client.post("/todos", json={"title": "Test Bearer Todo"}, headers=headers)
    assert todo_res.status_code == 201
    assert todo_res.json()["title"] == "Test Bearer Todo"






