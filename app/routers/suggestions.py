import os
import re
import sqlite3
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status

from app.database import get_connection
from app.schemas import StudyTipRead, StudyTipRequest, UserRead
from app.security import CurrentUser

router = APIRouter()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
MAX_OUTPUT_TOKENS = 48
MAX_GENERATION_ATTEMPTS = 3
RECENT_TIPS_IN_PROMPT = 3
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def _normalize_tip(tip: str) -> str:
    return re.sub(r"[\W_]+", " ", tip.casefold()).strip()


@router.post("/study-tip", response_model=StudyTipRead)
async def create_study_tip(
    tip_request: StudyTipRequest | None = None,
    user: UserRead = CurrentUser,
) -> StudyTipRead:
    if user.grade is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Set your school class before requesting a study tip.",
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Study tips are not configured. Set the GEMINI_API_KEY environment variable.",
        )

    subject_name = (tip_request.subject.strip() if tip_request and tip_request.subject else "General")
    model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
    with get_connection() as connection:
        seen_tips = {
            row["normalized_tip"]
            for row in connection.execute(
                "SELECT normalized_tip FROM study_tips WHERE user_id = ?",
                (user.id,),
            )
        }
        recent_tips = [
            row["tip"]
            for row in connection.execute(
                """
                SELECT tip FROM study_tips
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user.id, RECENT_TIPS_IN_PROMPT),
            )
        ]

    rejected_tips: list[str] = []
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            for _ in range(MAX_GENERATION_ATTEMPTS):
                excluded_tips = recent_tips + rejected_tips
                if subject_name.lower() != "general":
                    prompt = (
                        f"Give one practical study tip for a student studying {subject_name} in Class {user.grade}. "
                        "Use one sentence under 25 words. No greeting. Make it new: "
                        "choose a different technique and do not repeat or paraphrase a previous tip."
                    )
                else:
                    prompt = (
                        f"Give one practical study tip for a student in Class {user.grade}. "
                        "Use one sentence under 25 words. No greeting. Make it new: "
                        "choose a different subject or technique and do not repeat or "
                        "paraphrase a previous tip."
                    )
                if excluded_tips:
                    prompt += "\nPrevious tips to avoid: " + " | ".join(excluded_tips)

                response = await client.post(
                    f"{GEMINI_API_URL}/{model}:generateContent",
                    headers={"x-goog-api-key": api_key},
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {
                            "maxOutputTokens": MAX_OUTPUT_TOKENS,
                        },
                    },
                )
                response.raise_for_status()
                result = response.json()
                try:
                    tip = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                except (KeyError, IndexError, TypeError, AttributeError) as error:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail="Gemini did not return a study tip. Try again.",
                    ) from error

                normalized_tip = _normalize_tip(tip)
                if not normalized_tip:
                    continue
                if normalized_tip in seen_tips:
                    rejected_tips.append(tip)
                    continue

                try:
                    with get_connection() as connection:
                        connection.execute(
                            """
                            INSERT INTO study_tips
                                (user_id, tip, normalized_tip, subject)
                            VALUES (?, ?, ?, ?)
                            """,
                            (user.id, tip, normalized_tip, subject_name),
                        )
                except sqlite3.IntegrityError:
                    seen_tips.add(normalized_tip)
                    rejected_tips.append(tip)
                    continue

                return StudyTipRead(tip=tip)

    except httpx.TimeoutException as error:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Gemini took too long to respond. Try again.",
        ) from error
    except httpx.HTTPStatusError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Gemini could not generate a study tip. Try again later.",
        ) from error
    except (httpx.RequestError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not reach Gemini. Try again later.",
        ) from error

    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Gemini could not generate a new study tip. Try again.",
    )
