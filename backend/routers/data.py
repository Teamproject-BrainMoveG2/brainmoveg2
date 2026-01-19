import socketio
import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.cone_service import ConeService
from services.game_service import GameService
from dependencies import get_cone_service, get_settings, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository
from repositories.gamesession_repository import GameSessionRepository
from models.models import Cone, ConeStatusDTO
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/data",
    tags=["data"],
    dependencies=[Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.get("/today")
async def get_today_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_today(settings)
    except Exception as e:
        logger.error(f"Error retrieving today's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"data": data}

@router.get("/week")
async def get_week_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_thisweek(settings)
    except Exception as e:
        logger.error(f"Error retrieving this week's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"data": data}

@router.get("/month")
async def get_month_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_thismonth(settings)
    except Exception as e:
        logger.error(f"Error retrieving this month's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"data": data}

@router.get("/alltime")
async def get_alltime_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_alltime(settings)
    except Exception as e:
        logger.error(f"Error retrieving all-time data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"data": data}

