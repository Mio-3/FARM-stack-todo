from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import check_db_connection
from app.routes import todo

app = FastAPI(
  title="Todo API",
  description="Todo管理のためのRESTful API",
  version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    await check_db_connection()


app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],  # Viteのデフォルトポート
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


app.include_router(todo.router, prefix="/api")