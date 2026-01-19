import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.game_service import GameService
from dependencies import get_cone_service, get_game_service, get_settings, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository
from models.models import Cone, ConeDTO
from services.cone_service import ConeService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(get_game_service), Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.post("/start")
async def start_game(game_service: GameService = Depends(get_game_service), sio=Depends(get_sio), cone_service: ConeService = Depends(get_cone_service)):
    logger.info("Starting a new game via API.")
    try:
        result = await game_service.start_game(sio, cone_service)
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"message":result}

@router.post("/hit")
async def record_cone_hit(cone: ConeDTO, game_service: GameService = Depends(get_game_service), sio=Depends(get_sio), cone_service: ConeService = Depends(get_cone_service)):
    try:
        await game_service.record_round(cone.cone_id, sio, cone_service)
    except ValueError as ve:
        logger.error(f"Error recording cone hit: {ve}")
        raise HTTPException(status_code=400, detail="No round is in progress.")
    except Exception as e:
        logger.error(f"Error recording cone hit: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Cone {cone.cone_id} hit recorded."}


