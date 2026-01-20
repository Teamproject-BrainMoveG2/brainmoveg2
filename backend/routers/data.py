from datetime import date
from typing import Optional
from fastapi.responses import FileResponse
import socketio
import config
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.cone_service import ConeService
from services.export_service import ExportService
from services.game_service import GameService
from dependencies import get_cone_service, get_export_service, get_settings, get_sio
from repositories.mode_repository import ModeRepository
from repositories.tutorial_repository import TutorialRepository
from repositories.gamesession_repository import GameSessionRepository
from models.models import Cone, ConeStatusDTO, ExportDateDTO
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
        if data:
            avg_reaction_speed = sum(session['avg_reactietijd_ms'] for session in data) / len(data)
            avg_accuracy = sum(session['accuracy_percent'] for session in data) / len(data)
        else:
            avg_reaction_speed = 0
            avg_accuracy = 0
    except Exception as e:
        logger.error(f"Error retrieving today's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"avg_reaction_speed": avg_reaction_speed, "avg_accuracy": avg_accuracy, "data": data}
@router.get("/week")
async def get_week_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_thisweek(settings)
        if data:
            avg_reaction_speed = sum(session['avg_reactietijd_ms'] for session in data) / len(data)
            avg_accuracy = sum(session['accuracy_percent'] for session in data) / len(data)
        else:
            avg_reaction_speed = 0
            avg_accuracy = 0

    except Exception as e:
        logger.error(f"Error retrieving this week's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"avg_reaction_speed": avg_reaction_speed, "avg_accuracy": avg_accuracy, "data": data}

@router.get("/month")
async def get_month_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_thismonth(settings)
        if data:
            avg_reaction_speed = sum(session['avg_reactietijd_ms'] for session in data) / len(data)
            avg_accuracy = sum(session['accuracy_percent'] for session in data) / len(data)
        else:
            avg_reaction_speed = 0
            avg_accuracy = 0
    except Exception as e:
        logger.error(f"Error retrieving this month's data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"avg_reaction_speed": avg_reaction_speed, "avg_accuracy": avg_accuracy, "data": data}

@router.get("/alltime")
async def get_alltime_data(settings: Annotated[config.Settings, Depends(get_settings)]):
    try:
        data = GameSessionRepository.get_sessions_alltime(settings)
        if data:
            avg_reaction_speed = sum(session['avg_reactietijd_ms'] for session in data) / len(data)
            avg_accuracy = sum(session['accuracy_percent'] for session in data) / len(data)
        else:
            avg_reaction_speed = 0
            avg_accuracy = 0
    except Exception as e:
        logger.error(f"Error retrieving all-time data: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    return {"avg_reaction_speed": avg_reaction_speed, "avg_accuracy": avg_accuracy, "data": data}

@router.get("/excel")
async def get_excel_data(settings: Annotated[config.Settings, Depends(get_settings)], start: date, end: date = None, exportService: ExportService = Depends(get_export_service)):
    data = GameSessionRepository.get_sessions_in_date_range(settings, start, end)
    logger.info(f"Exporting data from {start} to {end}: {data}")
    file_path = exportService.export_data_to_excel(data)
    date_range = start.strftime('%Y%m%d') + '_to_' + end.strftime('%Y%m%d')
    filename = f'brainmove_export_{date_range}.xlsx'

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    

