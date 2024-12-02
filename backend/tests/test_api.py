# tests/test_api.py
import pytest
from httpx import AsyncClient
from app.main import app
from bson import ObjectId
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/todos/",
            json={
                "title": "テストタスク",
                "description": "これはテストです",
                "completed": False
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "テストタスク"
        assert "id" in data
        assert "created_at" in data


@pytest.mark.asyncio
async def test_get_todos():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # テストデータの作成
        await client.post(
            "/api/todos/",
            json={"title": "テストタスク1"}
        )
        await client.post(
            "/api/todos/",
            json={"title": "テストタスク2"}
        )

        response = await client.get("/api/todos/")
        assert response.status_code == 200
        todos = response.json()
        assert isinstance(todos, list)
        assert len(todos) >= 2


@pytest.mark.asyncio
async def test_read_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # テストデータの作成
        create_response = await client.post(
            "/api/todos/",
            json={
                "title": "テスト用Todo",
                "description": "個別取得のテスト"
            }
        )
        created_todo = create_response.json()
        todo_id = created_todo["id"]

        get_response = await client.get(f"/api/todos/{todo_id}")
        assert get_response.status_code == 200
        todo_data = get_response.json()

        assert todo_data["id"] == todo_id
        assert todo_data["title"] == "テスト用Todo"
        assert todo_data["description"] == "個別取得のテスト"


@pytest.mark.asyncio
async def test_read_todo_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        non_existent_id = str(ObjectId())
        response = await client.get(f"/api/todos/{non_existent_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_todo_invalid_id():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/todos/invalid-id")
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # テストデータの作成
        create_response = await client.post(
            "/api/todos/",
            json={
                "title": "更新前のタスク",
                "description": "これは更新されます"
            }
        )
        todo_id = create_response.json()["id"]

        update_response = await client.put(
            f"/api/todos/{todo_id}",
            json={
                "title": "更新後のタスク"
            }
        )
        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["title"] == "更新後のタスク"
        assert "description" in updated_todo


@pytest.mark.asyncio
async def test_delete_todo():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # テストデータの作成
        create_response = await client.post(
            "/api/todos/",
            json={
                "title": "削除するタスク"
            }
        )
        todo_id = create_response.json()["id"]

        # 削除の実行
        delete_response = await client.delete(f"/api/todos/{todo_id}")
        assert delete_response.status_code == 204

        # 削除の確認
        get_response = await client.get(f"/api/todos/{todo_id}")
        assert get_response.status_code == 404