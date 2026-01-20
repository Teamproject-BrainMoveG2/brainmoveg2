from services.cone_service import ConeService
from services.export_service import ExportService
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

async def get_export_service() -> ExportService:
    return ExportService()

# async def get_mqtt_service(settings: Annotated[config.Settings, Depends(get_settings)]) -> MQTTService:
#     mqtt = MQTTService(
#         broker_host=settings.mqtt_broker,
#         broker_port=settings.mqtt_port,
#         username=settings.mqtt_username,
#         password=settings.mqtt_password
#     )
#     mqtt.connect()
#     return mqtt

async def get_buzzer_service() -> BuzzerService:
    return BuzzerService()

async def get_sio(request: Request) -> socketio.AsyncServer:
    return request.app.state.sio

@lru_cache
def get_settings():
    return config.Settings()