# backend/app/models/todo.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId


class TodoCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Todoのタイトル"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Todoの説明"
    )
    completed: bool = Field(
        False,
        description="Todoの完了状態"
    )

    @validator("title")
    def title_must_contain_word_todo(cls, v):
        if any(word in v for word in ['<', '>', '&', '"', "'"]):
            raise ValueError("特殊文字を含めることはできません")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Todoのタイトル",
                "description": "Todoの説明",
                "completed": False
            }
        }


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "5f4a3f5f7b5b1f2b7a1f2b7a",
                "title": "プログラミング、アルゴリズムの勉強",
                "description": "フルスタック開発、LeetCode",
                "completed": False,
                "created_at": "2024-12-01T12:00:00",
                "updated_at": "2024-12-02T14:00:00"
            }
        }