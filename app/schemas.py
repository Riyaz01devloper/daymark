import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AccountRegister(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(max_length=6)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address")
        return value

    @field_validator("password")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if len(value) != 6 or not value.isascii() or not value.isdigit():
            raise ValueError("PIN must contain exactly 6 digits")
        return value


class AccountLogin(BaseModel):
    email: str = Field(min_length=3, max_length=254)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        value = value.strip().lower()
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", value):
            raise ValueError("Enter a valid email address")
        return value


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1, max_length=128)
    new_password: str = Field(max_length=6)

    @field_validator("new_password")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if len(value) != 6 or not value.isascii() or not value.isdigit():
            raise ValueError("PIN must contain exactly 6 digits")
        return value


class UserRead(BaseModel):
    id: int
    email: str
    grade: int | None = None
    language: str = "en"
    token: str | None = None


class ProfileUpdate(BaseModel):
    grade: int | None = Field(default=None, ge=1, le=12)
    language: Literal["en", "hi", "english", "hindi"] | None = None


class GradeUpdate(ProfileUpdate):
    pass


class StudyTipRequest(BaseModel):
    subject: str = Field(default="General", max_length=50)


class StudyTipRead(BaseModel):
    tip: str


TodoPriority = Literal["low", "medium", "high"]


class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    completed: bool = False
    priority: TodoPriority = "medium"
    due_date: str | None = Field(default=None, max_length=20)
    category: str = Field(default="General", max_length=50)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be blank")
        return value

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str) -> str:
        value = value.strip()
        return value if value else "General"


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    completed: bool | None = None
    priority: TodoPriority | None = None
    due_date: str | None = Field(default=None, max_length=20)
    category: str | None = Field(default=None, max_length=50)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            if not value:
                raise ValueError("Title cannot be blank")
        return value

    @field_validator("category")
    @classmethod
    def normalize_category(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()
            return value if value else "General"
        return value


class TodoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    created_at: str
    priority: TodoPriority = "medium"
    due_date: str | None = None
    category: str = "General"


class TodoSummary(BaseModel):
    total: int
    active: int
    completed: int


TodoStatus = Literal["all", "active", "completed"]


class UserSubjectsUpdate(BaseModel):
    subjects: list[str] = Field(min_length=1, max_length=20)


class UserSubjectsRead(BaseModel):
    subjects: list[str]
    default_subjects: list[str]


class CurriculumResponse(BaseModel):
    class_grade: int
    language: str = "en"
    curriculum: dict[str, list[str]]


class PyqRead(BaseModel):
    id: int
    class_grade: int
    subject: str
    chapter: str
    year: int
    exam_type: str
    marks: int
    question: str
    answer: str


class GenerateNotesRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=100)
    chapter: str = Field(min_length=1, max_length=200)
    note_type: Literal["comprehensive", "quick_revision", "formula_summary"] = "comprehensive"
    language: Literal["en", "hi", "english", "hindi"] = "en"


class GeneratedNoteRead(BaseModel):
    id: int
    class_grade: int
    subject: str
    chapter: str
    title: str
    content: str
    created_at: str


class OfficialResourcesRead(BaseModel):
    class_grade: int
    title: str
    board_pyq_url: str
    sqp_2024_25_url: str
    sqp_2023_24_url: str
    sqp_2022_23_url: str
    question_bank_url: str
    ncert_books_url: str
    ncert_ebooks_url: str
    ncert_exemplar_url: str
    curriculum_url: str
    language: str = "en"


class ChapterResourceRead(BaseModel):
    class_grade: int
    subject: str
    chapter: str
    language: str = "en"
    summary_notes: str
    key_takeaways: list[str]
    animation_video_url: str
    diksha_video_url: str
    khan_academy_url: str
    ncert_book_url: str
    english_chapter: str | None = None
    english_subject: str | None = None




