import os
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.database import get_connection
from app.ncert_data import (
    NCERT_CURRICULUM,
    get_chapter_resource,
    get_chapter_resources_for_subject,
    get_chapters_for_grade_subject,
    get_curriculum_for_grade,
    get_official_resources_for_grade,
    get_subjects_for_grade,
)
from app.schemas import (
    ChapterResourceRead,
    CurriculumResponse,
    GenerateNotesRequest,
    GeneratedNoteRead,
    OfficialResourcesRead,
    PyqRead,
    UserRead,
    UserSubjectsRead,
    UserSubjectsUpdate,
)
from app.security import CurrentUser

router = APIRouter()
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"


@router.get("/subjects", response_model=UserSubjectsRead)
def get_user_subjects(user: UserRead = CurrentUser) -> UserSubjectsRead:
    defaults = get_subjects_for_grade(user.grade)
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT subject FROM user_subjects WHERE user_id = ? ORDER BY id",
            (user.id,),
        ).fetchall()
        user_subjects = [row["subject"] for row in rows]

    return UserSubjectsRead(
        subjects=user_subjects if user_subjects else defaults,
        default_subjects=defaults,
    )


@router.put("/subjects", response_model=UserSubjectsRead)
def update_user_subjects(
    data: UserSubjectsUpdate, user: UserRead = CurrentUser
) -> UserSubjectsRead:
    clean_subjects: list[str] = []
    for item in data.subjects:
        clean = item.strip()
        if clean and clean not in clean_subjects:
            clean_subjects.append(clean)

    if not clean_subjects:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Select at least one subject.",
        )

    with get_connection() as connection:
        connection.execute(
            "DELETE FROM user_subjects WHERE user_id = ?", (user.id,)
        )
        for sub in clean_subjects:
            connection.execute(
                "INSERT INTO user_subjects (user_id, subject) VALUES (?, ?)",
                (user.id, sub),
            )

    return UserSubjectsRead(
        subjects=clean_subjects,
        default_subjects=get_subjects_for_grade(user.grade),
    )


@router.get("/curriculum", response_model=CurriculumResponse)
def get_curriculum(
    user: UserRead = CurrentUser,
    class_grade: Annotated[int | None, Query(ge=1, le=12)] = None,
    language: Annotated[str | None, Query(max_length=20)] = None,
) -> CurriculumResponse:
    grade = class_grade or user.grade or 10
    lang = (language or user.language or "en").strip().lower()
    selected_lang = "hi" if lang in ("hi", "hindi") else "en"
    curriculum = get_curriculum_for_grade(grade, language=selected_lang)
    if not curriculum:
        curriculum = {sub: [] for sub in get_subjects_for_grade(grade, language=selected_lang)}

    return CurriculumResponse(
        class_grade=grade, language=selected_lang, curriculum=curriculum
    )


@router.get("/official-resources", response_model=OfficialResourcesRead)
def get_official_resources(
    user: UserRead = CurrentUser,
    class_grade: Annotated[int | None, Query(ge=1, le=12)] = None,
    language: Annotated[str | None, Query(max_length=20)] = None,
) -> OfficialResourcesRead:
    grade = class_grade or user.grade or 10
    lang = (language or user.language or "en").strip().lower()
    selected_lang = "hi" if lang in ("hi", "hindi") else "en"
    res = get_official_resources_for_grade(grade, language=selected_lang)
    res["language"] = selected_lang
    return OfficialResourcesRead(**res)


@router.get("/chapter-resources", response_model=list[ChapterResourceRead])
def get_chapter_resources(
    user: UserRead = CurrentUser,
    class_grade: Annotated[int | None, Query(ge=1, le=12)] = None,
    subject: Annotated[str, Query(max_length=100)] = "",
    chapter: Annotated[str, Query(max_length=200)] = "",
    language: Annotated[str | None, Query(max_length=20)] = None,
) -> list[ChapterResourceRead]:
    grade = class_grade or user.grade or 10
    lang = (language or user.language or "en").strip().lower()
    selected_lang = "hi" if lang in ("hi", "hindi") else "en"
    resources = get_chapter_resources_for_subject(
        grade=grade, subject=subject, chapter=chapter, language=selected_lang
    )
    return [ChapterResourceRead(**item) for item in resources]




@router.get("/pyqs", response_model=list[PyqRead])
def get_pyqs(
    user: UserRead = CurrentUser,
    class_grade: Annotated[int | None, Query(ge=1, le=12)] = None,
    subject: Annotated[str, Query(max_length=100)] = "",
    year: Annotated[int | None, Query(ge=2000, le=2030)] = None,
    chapter: Annotated[str, Query(max_length=200)] = "",
) -> list[PyqRead]:
    grade = class_grade or user.grade or 10
    conditions = ["class_grade = ?"]
    params: list[object] = [grade]

    if subject:
        conditions.append("LOWER(subject) = LOWER(?)")
        params.append(subject.strip())
    if year:
        conditions.append("year = ?")
        params.append(year)
    if chapter:
        conditions.append("LOWER(chapter) LIKE LOWER(?)")
        params.append(f"%{chapter.strip()}%")

    query = (
        "SELECT id, class_grade, subject, chapter, year, exam_type, marks, question, answer "
        f"FROM pyqs WHERE {' AND '.join(conditions)} ORDER BY year DESC, id DESC LIMIT 50"
    )

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()

    return [
        PyqRead(
            id=row["id"],
            class_grade=row["class_grade"],
            subject=row["subject"],
            chapter=row["chapter"],
            year=row["year"],
            exam_type=row["exam_type"],
            marks=row["marks"],
            question=row["question"],
            answer=row["answer"],
        )
        for row in rows
    ]


@router.post("/generate-notes", response_model=GeneratedNoteRead)
async def generate_ncert_notes(
    request: GenerateNotesRequest,
    user: UserRead = CurrentUser,
) -> GeneratedNoteRead:
    grade = user.grade or 10
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI Note generation is not configured. Set GEMINI_API_KEY.",
        )

    model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

    if request.language in ("hi", "hindi"):
        prompt = (
            f"आप एक विशेषज्ञ NCERT शिक्षक हैं। कक्षा {grade} के विषय '{request.subject}', अध्याय: '{request.chapter}' "
            f"के लिए आधिकारिक NCERT हिंदी पाठ्यपुस्तक के अनुसार उच्च-अंक पुनरावृत्ति नोट्स तैयार करें।\n\n"
            f"निम्नलिखित शीर्षकों के साथ स्वच्छ Markdown में उत्तर दें:\n"
            f"1. **अध्याय का अवलोकन एवं मूल अवधारणाएँ** (बुलेट पॉइंट्स में)\n"
            f"2. **मुख्य परिभाषाएँ, महत्वपूर्ण सूत्र एवं समीकरण**\n"
            f"3. **NCERT परीक्षा के महत्वपूर्ण बिंदु (हाई-यील्ड)**\n"
            f"4. **स्व-मूल्यांकन हेतु 2-3 अभ्यास प्रश्न (संक्षिप्त संकेत सहित)**\n\n"
            f"भाषा शुद्ध, स्पष्ट, छात्र-हितैषी तथा NCERT पाठ्यपुस्तक की शब्दावली के पूर्णतः अनुरूप होनी चाहिए।"
        )
    else:
        prompt = (
            f"You are an expert NCERT educator. Create structured, high-yield study revision notes for "
            f"Class {grade} {request.subject}, Chapter: '{request.chapter}' according to the latest NCERT curriculum.\n\n"
            f"Format your response in clean Markdown with the following sections:\n"
            f"1. **Chapter Overview & Core Concepts** (brief bullet points)\n"
            f"2. **Key Definitions & Important Formulas / Equations**\n"
            f"3. **NCERT High-Yield & Exam-Favorite Points**\n"
            f"4. **Quick Self-Assessment (2-3 Practice Questions with brief hints)**\n\n"
            f"Be accurate, concise, student-friendly, and faithful to standard NCERT textbook content."
        )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                f"{GEMINI_API_URL}/{model}:generateContent",
                headers={"x-goog-api-key": api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": 1024,
                        "temperature": 0.4,
                    },
                },
            )
            response.raise_for_status()
            result = response.json()
            notes_content = (
                result["candidates"][0]["content"]["parts"][0]["text"].strip()
            )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Could not generate NCERT notes via Gemini: {error}",
        ) from error

    title = f"Class {grade} {request.subject} - {request.chapter}"
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO generated_notes (user_id, class_grade, subject, chapter, title, content)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user.id, grade, request.subject, request.chapter, title, notes_content),
        )
        note_id = cursor.lastrowid
        row = connection.execute(
            "SELECT id, class_grade, subject, chapter, title, content, created_at "
            "FROM generated_notes WHERE id = ?",
            (note_id,),
        ).fetchone()

    return GeneratedNoteRead(
        id=row["id"],
        class_grade=row["class_grade"],
        subject=row["subject"],
        chapter=row["chapter"],
        title=row["title"],
        content=row["content"],
        created_at=row["created_at"],
    )


@router.get("/notes", response_model=list[GeneratedNoteRead])
def get_user_notes(user: UserRead = CurrentUser) -> list[GeneratedNoteRead]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, class_grade, subject, chapter, title, content, created_at
            FROM generated_notes
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user.id,),
        ).fetchall()

    return [
        GeneratedNoteRead(
            id=row["id"],
            class_grade=row["class_grade"],
            subject=row["subject"],
            chapter=row["chapter"],
            title=row["title"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_note(
    note_id: int, user: UserRead = CurrentUser
) -> Response:
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM generated_notes WHERE id = ? AND user_id = ?",
            (note_id, user.id),
        )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
