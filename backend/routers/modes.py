import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.game_service import GameService
from dependencies import get_game_service, get_settings, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository

from models.models import Cone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/modes",
    tags=["modes"],
    dependencies=[Depends(get_game_service), Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_game_modes(settings: Annotated[config.Settings, Depends(get_settings)],):
    modes = ModeRepository.get_all_modes(settings=settings)
    return modes

@router.get("/{mode_id}/tutorial")
async def get_tutorial_for_mode(mode_id: int, settings: Annotated[config.Settings, Depends(get_settings)],):
    rounds = TutorialRepository.get_rondes_by_mode_id(settings=settings, mode_id=mode_id)
    if not rounds:
        raise HTTPException(status_code=404, detail="Game mode not found.")
    return rounds
   