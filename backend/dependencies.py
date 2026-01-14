from services.game_service import GameService
from fastapi import Depends, Request
import socketio
from functools import lru_cache
import config

async def get_game_service() -> GameService:
    return GameService()

async def get_sio(request:Request) -> socketio.AsyncServer:
    return request.app.state.sio

@lru_cache
def get_settings():
    return config.Settings()