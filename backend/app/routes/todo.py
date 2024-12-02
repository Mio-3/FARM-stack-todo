# app/routes/todo.py
from fastapi import APIRouter, HTTPException, status
from app.model.todo import TodoCreate, TodoUpdate, TodoResponse
from app.database import collection  
from bson import ObjectId
from typing import List
from datetime import datetime

router = APIRouter()


@router.post("/todos/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    todo_dict = todo.dict()
    todo_dict["created_at"] = datetime.now()
    result = await collection.insert_one(todo_dict)
    created_todo = await collection.find_one({"_id": result.inserted_id})
    return {**created_todo, "id": str(created_todo["_id"])}


@router.get("/todos/", response_model=List[TodoResponse])
async def read_todos():
    todos = await collection.find().to_list(1000)
    return [{**todo, "id": str(todo["_id"])} for todo in todos]


@router.get("/todos/{todo_id}", response_model=TodoResponse)
async def read_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    todo = await collection.find_one({"_id": ObjectId(todo_id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {**todo, "id": str(todo["_id"])}


@router.put("/todos/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo: TodoUpdate):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")

    result = await collection.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    updated_todo = await collection.find_one({"_id": ObjectId(todo_id)})
    return {**updated_todo, "id": str(updated_todo["_id"])}


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")