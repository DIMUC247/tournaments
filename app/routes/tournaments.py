from fastapi import APIRouter

from app.db.tournaments import db_actions


tournaments_router = APIRouter(prefix="/tournaments", tags=["Tournament"])