from fastapi.concurrency import run_in_threadpool
import socketio
from fastapi import APIRouter, Depends
from services.cone_service import ConeService
from dependencies import get_cone_service, get_mqtt_service, get_sio
from models.models import ConeStatusDTO, ConeStatus, StatusMessage
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

@router.get("", response_model=list[ConeStatus])
async def get_status_cones(cone_service: ConeService = Depends(get_cone_service)):
    cones = cone_service.get_cones()
    return cones
