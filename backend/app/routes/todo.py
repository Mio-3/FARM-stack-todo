from fastapi import APIRouter, HTTPException, status
from app.model.todo import Todo, TodoCreate, TodoUpdate
from app.database import collection
from bson import ObjectId
from typing import List

router = APIRouter()


@router.post("/todos/", response_model=List[Todo])
async def create_todos(todo: TodoCreate):
    todo_dict = todo.dict()
    new_todo = Todo(**todo_dict)
    await collection.insert_one(new_todo.dict(by_alias=True))
    return new_todo


@router.get("/todos/", response_model=List[Todo])
async def read_todos():
    todos = await collection.find().to_list(1000)
    return [Todo(**todo) for todo in todos]


@router.get("/todos/{id}", response_model=Todo)
async def read_todo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    todo = await collection.find_one({"_id": ObjectId(id)})
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Todo(**todo)


@router.put("/todos/{id}", response_model=Todo)
async def update_todo(id: str, todo: TodoUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    update_data = {k: v for k, v in todo.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")
    
    result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )
    
    if not result.modified_count:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    update_todo = await collection.find_one({"_id": ObjectId(id)})
    return Todo(**update_todo)


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if not ObjectId.is_valid(todo_id):
        raise HTTPException(status_code=400, detail="Invalid todo ID")
    
    result = await collection.delete_one({"_id": ObjectId(todo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
