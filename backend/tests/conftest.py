# tests/conftest.py
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import asyncio
from app.database import collection

load_dotenv()


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_test_db():
    # テスト実行前にデータベースをクリーンアップ
    await collection.delete_many({})
    yield
    # テスト実行後にもクリーンアップ
    await collection.delete_many({})