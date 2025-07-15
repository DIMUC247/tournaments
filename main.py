import asyncio

from fastapi import FastAPI
import uvicorn


from app.db.base import create_db


if __name__ == "__main__":
    # asyncio.run(create_db())
    uvicorn.run("main:app",reload=True)