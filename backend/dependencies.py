from services.game_service import GameService
from fastapi import Depends, Request
import socketio

async def get_game_service() -> GameService:
    return GameService()

async def get_sio(request:Request) -> socketio.AsyncServer:
    return request.app.state.sio
