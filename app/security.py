import hashlib
import hmac
import secrets
import time

from fastapi import Cookie, Depends, HTTPException, Request, Response, status

from app.database import get_connection
from app.schemas import UserRead

SESSION_COOKIE = "todo_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 7
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=32,
    )
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, n, r, p, salt_hex, digest_hex = encoded_hash.split("$")
        if algorithm != "scrypt":
            return False
        candidate = hashlib.scrypt(
            password.encode("utf-8"),
            salt=bytes.fromhex(salt_hex),
            n=int(n),
            r=int(r),
            p=int(p),
            dklen=len(bytes.fromhex(digest_hex)),
        )
        return hmac.compare_digest(candidate.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


def _token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_session(user_id: int, response: Response, request: Request) -> str:
    token = secrets.token_urlsafe(32)
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (_token_digest(token), user_id, int(time.time()) + SESSION_MAX_AGE),
        )
    is_https = (
        request.url.scheme == "https"
        or request.headers.get("x-forwarded-proto", "").lower() == "https"
    )
    samesite_policy = "none" if is_https else "lax"
    response.set_cookie(
        key=SESSION_COOKIE,
        value=token,
        max_age=SESSION_MAX_AGE,
        httponly=True,
        secure=is_https,
        samesite=samesite_policy,
        path="/",
    )
    response.headers["X-Session-Token"] = token
    return token


def delete_session(
    token: str | None,
    response: Response,
    request: Request | None = None,
    is_https: bool = False,
) -> None:
    extracted_token = token
    if not extracted_token and request:
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            extracted_token = auth_header[7:].strip()
        elif request.headers.get("x-session-token"):
            extracted_token = request.headers.get("x-session-token").strip()

    if extracted_token:
        with get_connection() as connection:
            connection.execute(
                "DELETE FROM sessions WHERE token_hash = ?", (_token_digest(extracted_token),)
            )
    samesite_policy = "none" if is_https else "lax"
    response.delete_cookie(
        key=SESSION_COOKIE,
        httponly=True,
        secure=is_https,
        samesite=samesite_policy,
        path="/",
    )


def get_current_user(
    request: Request,
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE),
) -> UserRead:
    # 1. Check Authorization Bearer header
    auth_header = request.headers.get("authorization", "")
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif request.headers.get("x-session-token"):
        token = request.headers.get("x-session-token").strip()
    elif session_token:
        token = session_token

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sign in to continue"
        )

    with get_connection() as connection:
        user_columns = {row["name"] for row in connection.execute("PRAGMA table_info(users)")}
        has_lang = "language" in user_columns
        lang_col = ", users.language" if has_lang else ""
        row = connection.execute(
            f"""
            SELECT users.id, users.email, users.grade{lang_col}
            FROM sessions
            JOIN users ON users.id = sessions.user_id
            WHERE sessions.token_hash = ? AND sessions.expires_at > ?
            """,
            (_token_digest(token), int(time.time())),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
        )
    user_lang = row["language"] if has_lang and row["language"] else "en"
    return UserRead(
        id=row["id"], email=row["email"], grade=row["grade"], language=user_lang, token=token
    )


CurrentUser = Depends(get_current_user)
