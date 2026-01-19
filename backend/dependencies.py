from services.cone_service import ConeService
from services.game_service import GameService
from services.score_service import ScoreService
from services.mqtt_service import MQTTService
from services.buzzer_service import BuzzerService
from fastapi import Depends, Request
import socketio
from functools import lru_cache
import config
from typing import Annotated

async def get_game_service() -> GameService:
    return GameService()

async def get_cone_service() -> ConeService:
    return ConeService()

async def get_score_service() -> ScoreService:
    return ScoreService()

async def get_mqtt_service(request: Request) -> MQTTService:
    return request.app.state.mqtt

async def get_buzzer_service() -> BuzzerService:
    return BuzzerService()

async def get_sio(request: Request) -> socketio.AsyncServer:
    return request.app.state.sio

@lru_cache
def get_settings():
    return config.Settings()