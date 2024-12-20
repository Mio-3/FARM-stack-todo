from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import check_db_connection
from app.routes import todo
from contextlib import asynccontextmanager

app = FastAPI(
  title="Todo API",
  description="Todo管理のためのRESTful API",
  version="1.0.0"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await check_db_connection()
    yield

origins = [
  "http://localhost:5173",
  "http://127.0.0.1:5173"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,  # Viteのデフォルトポート
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
  expose_headers=["*"],
)


app.include_router(todo.router, prefix="/api")