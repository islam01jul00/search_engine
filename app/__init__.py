from dotenv import load_dotenv

load_dotenv()

from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.db import engine
from app.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(router)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail
        }
    )

@app.exception_handler(Exception)
def custom_exception_handler(request: Request, exception: Exception):
    print(exception)

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Unexpected error has been occurred."
        }
    )
