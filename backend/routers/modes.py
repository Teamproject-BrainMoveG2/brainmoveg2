from fastapi.concurrency import run_in_threadpool
import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_game_service, get_settings, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository
from models.models import GameMode, ModeTutorial
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/modes",
    tags=["modes"],
    dependencies=[Depends(get_game_service), Depends(get_sio)],
    responses={404: {"description": "Not found"}},
)

@router.get("/",  response_model=list[GameMode])
async def get_game_modes(settings: Annotated[config.Settings, Depends(get_settings)],):
    modes = await run_in_threadpool(ModeRepository.get_all_modes, settings)
    return modes

@router.get("/{mode_id}/tutorial", response_model=ModeTutorial)
async def get_tutorial_for_mode(mode_id: int, settings: Annotated[config.Settings, Depends(get_settings)],):
    mode = await run_in_threadpool(ModeRepository.get_mode_by_id, settings, mode_id)
    steps = await run_in_threadpool(TutorialRepository.get_rondes_by_mode_id, settings, mode_id)
    if not steps:
        raise HTTPException(status_code=404, detail="Game mode not found.")
    steps_data = []
    for step in steps:
        steps_data.append({
            "number": step["number"],
            "description": step["description"],
        })
    return {"image": mode["image"], "steps": steps_data }
   