import sqlite3
import time
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status

from app.database import get_connection
from app.schemas import (
    AccountLogin,
    AccountRegister,
    GradeUpdate,
    PasswordChange,
    ProfileUpdate,
    UserRead,
)
from app.security import (
    SESSION_COOKIE,
    CurrentUser,
    create_session,
    delete_session,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter()
LOGIN_WINDOW_SECONDS = 15 * 60
LOGIN_MAX_ATTEMPTS = 10


@router.post(
    "/register", response_model=UserRead, status_code=status.HTTP_201_CREATED
)
def register(account: AccountRegister) -> UserRead:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO users (email, password_hash, created_at) "
                "VALUES (?, ?, datetime('now'))",
                (account.email, hash_password(account.password)),
            )
            user_id = cursor.lastrowid
    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from error

    return UserRead(id=user_id, email=account.email)


@router.post("/login", response_model=UserRead)
def login(account: AccountLogin, request: Request, response: Response) -> UserRead:
    with get_connection() as connection:
        now = int(time.time())
        connection.execute("DELETE FROM login_attempts WHERE attempted_at <= ?", (now - LOGIN_WINDOW_SECONDS,))
        attempts = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM login_attempts
            WHERE email = ? AND attempted_at > ?
            """,
            (account.email, now - LOGIN_WINDOW_SECONDS),
        ).fetchone()["total"]
        if attempts >= LOGIN_MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many sign-in attempts. Try again in 15 minutes.",
            )

        user_columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)")}
        has_lang = "language" in user_columns
        lang_col = ", language" if has_lang else ""
        row = connection.execute(
            f"SELECT id, email, password_hash, grade{lang_col} FROM users WHERE email = ?",
            (account.email,),
        ).fetchone()

    if row is None or not verify_password(account.password, row["password_hash"]):
        with get_connection() as connection:
            connection.execute(
                "INSERT INTO login_attempts (email, attempted_at) VALUES (?, ?)",
                (account.email, int(time.time())),
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email or password is incorrect",
        )

    with get_connection() as connection:
        connection.execute("DELETE FROM login_attempts WHERE email = ?", (account.email,))
    token = create_session(row["id"], response, request)
    user_lang = row["language"] if has_lang and row["language"] else "en"
    return UserRead(
        id=row["id"], email=row["email"], grade=row["grade"], language=user_lang, token=token
    )


@router.get("/me", response_model=UserRead)
def who_am_i(user: UserRead = CurrentUser) -> UserRead:
    return user


@router.patch("/profile", response_model=UserRead)
def update_profile(
    profile_data: ProfileUpdate, user: UserRead = CurrentUser
) -> UserRead:
    updates: list[str] = []
    params: list[object] = []
    if profile_data.grade is not None:
        updates.append("grade = ?")
        params.append(profile_data.grade)
    if profile_data.language is not None:
        lang_val = "hi" if profile_data.language in ("hi", "hindi") else "en"
        updates.append("language = ?")
        params.append(lang_val)

    if updates:
        params.append(user.id)
        with get_connection() as connection:
            connection.execute(
                f"UPDATE users SET {', '.join(updates)} WHERE id = ?",
                tuple(params),
            )
            user_columns = {
                row["name"] for row in connection.execute("PRAGMA table_info(users)")
            }
            has_lang = "language" in user_columns
            lang_col = ", language" if has_lang else ""
            row = connection.execute(
                f"SELECT id, email, grade{lang_col} FROM users WHERE id = ?",
                (user.id,),
            ).fetchone()
        user_lang = row["language"] if has_lang and row["language"] else "en"
        return UserRead(
            id=row["id"], email=row["email"], grade=row["grade"], language=user_lang
        )

    return user


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(
    password_data: PasswordChange,
    user: UserRead = CurrentUser,
) -> Response:
    with get_connection() as connection:
        row = connection.execute(
            "SELECT password_hash FROM users WHERE id = ?",
            (user.id,),
        ).fetchone()
        if row is None or not verify_password(password_data.current_password, row["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current PIN/password is incorrect",
            )
        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (hash_password(password_data.new_password), user.id),
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: Request,
    response: Response,
    session_token: Annotated[str | None, Cookie(alias=SESSION_COOKIE)] = None,
) -> Response:
    delete_session(session_token, response, request=request)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response
