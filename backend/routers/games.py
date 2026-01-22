from services.mqtt_service import MQTTService
import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.game_service import GameService
from dependencies import get_cone_service, get_game_service, get_mqtt_service, get_score_service, get_settings, get_sio, get_buzzer_service
from models.models import ConeDTO, GameStartDTO, GameStatus, StatusMessage
from services.cone_service import ConeService
import logging
from services.score_service import ScoreService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/games",
    tags=["games"],
    dependencies=[Depends(get_game_service), Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.get("/status", response_model=GameStatus)
async def get_game_status(game_service: GameService = Depends(get_game_service)):
    status = await game_service.get_game_in_progress()
    return {"game_in_progress": status}

@router.post("/start", response_model=StatusMessage)
async def start_game(gameStart: GameStartDTO, settings: Annotated[config.Settings, Depends(get_settings)], mqtt_service: MQTTService = Depends(get_mqtt_service), game_service: GameService = Depends(get_game_service), sio=Depends(get_sio), cone_service: ConeService = Depends(get_cone_service), buzzer_service = Depends(get_buzzer_service)):
    logger.info("Starting a new game via API.")
    try:
        result = await game_service.start_game(gameStart.username, gameStart.mode_id, gameStart.difficulty_id, gameStart.aantal_rondes, gameStart.aantal_kleuren, sio, cone_service, settings, buzzer_service, mqtt_service)
    except Exception as e:
        logger.error(f"Error starting game: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"message":result}

@router.post("/stop", response_model=StatusMessage)
async def stop_game(settings: Annotated[config.Settings, Depends(get_settings)], game_service: GameService = Depends(get_game_service), sio=Depends(get_sio), cone_service: ConeService = Depends(get_cone_service)):
    logger.info("Stopping the current game.")
    try:
        await game_service.stop_game(sio, cone_service, settings)
    except Exception as e:
        logger.error(f"Error stopping game: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"message":"Game stopped successfully."}

@router.post("/hit", response_model=StatusMessage)
async def record_cone_hit(cone: ConeDTO, settings: Annotated[config.Settings, Depends(get_settings)], mqtt_service: MQTTService = Depends(get_mqtt_service), game_service: GameService = Depends(get_game_service), sio=Depends(get_sio), cone_service: ConeService = Depends(get_cone_service), score_service: ScoreService = Depends(get_score_service), buzzer_service = Depends(get_buzzer_service)):
    try:
        await game_service.record_round(cone.cone_id, sio, cone_service, score_service, settings, buzzer_service, mqtt_service)
    except ValueError as ve:
        logger.error(f"Error recording cone hit: {ve}")
        raise HTTPException(status_code=400, detail="No round is in progress.")
    except Exception as e:
        logger.error(f"Error recording cone hit: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"Cone {cone.cone_id} hit recorded."}


