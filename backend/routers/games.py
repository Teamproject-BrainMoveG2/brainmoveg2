from fastapi import APIRouter, Depends, HTTPException
from services.game_service import GameService
from dependencies import get_game_service, get_sio

from models.models import Cone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(get_game_service), Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.post("/start")
async def start_game(game_service: GameService = Depends(get_game_service), sio=Depends(get_sio)):
    logger.info("Starting a new game via API.")
    result = await game_service.start_game(sio)
    return {"message":result}

@router.post("/cone")
async def record_cone_hit(cone: Cone, game_service: GameService = Depends(get_game_service), sio=Depends(get_sio)):
    await game_service.record_round(cone, sio)
    return {"message": f"Cone {cone.cone_id} hit recorded."}