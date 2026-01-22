from fastapi.concurrency import run_in_threadpool
import socketio
import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.cone_service import ConeService
from services.game_service import GameService
from dependencies import get_cone_service, get_mqtt_service, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository

from models.models import ConeStatusDTO, StatusMessage
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cones",
    tags=["cones"],
    dependencies=[Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.post("/status", response_model=StatusMessage)
async def give_cone_status(cone: ConeStatusDTO, cone_service: ConeService = Depends(get_cone_service), sio: socketio.AsyncServer = Depends(get_sio), mqtt_service = Depends(get_mqtt_service)):
    await cone_service.register_cone(cone, sio)
    await run_in_threadpool(mqtt_service.connect)
    logger.info(f"Cone status received: {cone}")
    return {"message": f"Cone {cone.cone_id} status recorded."}

@router.get("/", response_model=list[ConeStatusDTO])
async def get_status_cones(cone_service: ConeService = Depends(get_cone_service)):
    cones = cone_service.get_cones()
    return cones
