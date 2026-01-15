import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.cone_service import ConeService
from services.game_service import GameService
from dependencies import get_cone_service, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository

from models.models import Cone, ConeStatusDTO
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/cones",
    tags=["cones"],
    dependencies=[Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.post("/status")
async def give_cone_status(cone: ConeStatusDTO, cone_service: ConeService = Depends(get_cone_service)):
    cone_service.register_cone(cone)
    logger.info(f"Cone status received: {cone}")
    return {"message": f"Cone {cone.cone_id} status recorded."}

@router.get("/")
async def get_status_cones(cone_service: ConeService = Depends(get_cone_service)):
    cones = cone_service.get_cones()
    return cones
