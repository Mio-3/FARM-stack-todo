import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
DATEBASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[DATEBASE_NAME]
collection = db[COLLECTION_NAME]


async def check_db_connection():
    try:
        await client.admin.command("ping")
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Unable to connect to MongoDB: {e}")