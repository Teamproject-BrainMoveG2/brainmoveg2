from typing_extensions import Annotated
import config
from models.models import Round, RoundResult, Cone, GameOverStats
from datetime import datetime, timezone
from services.cone_service import ConeService 
from services.score_service import ScoreService
from repositories.ronde_repository import RondeRepository
from repositories.gamesession_repository import GameSessionRepository
from fastapi import Depends
import random
import socketio
import logging
import asyncio

TOO_LATE = {1: 5000, 2: 4000, 3: 3000}
TOO_LATE_MS = 5000
maxRounds = 10
maxCones = 4
difficulty = 1
connectedCones = []
roundList = []
currentRoundStartTime = None
currentCone = None
totalTimeMs = 0
session_id = None
class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("GameService initialized.")


    async def start_game(self, username: str, mode_id: int, difficulty_id: int, aantal_rondes: int, aantal_kleuren: int, sio: socketio.AsyncServer, coneService: ConeService, settings: config.Settings) -> str:
        global session_id, maxRounds, maxCones, difficulty, TOO_LATE_MS
        self.logger.info("Game started.")
        if len(roundList) > 0 or currentRoundStartTime is not None or currentCone is not None:
            self.logger.warning("Game is already in progress. Cannot start a new game.")
            raise Exception("Game is already in progress. Cannot start a new game.")
        maxRounds = aantal_rondes
        maxCones = aantal_kleuren
        difficulty = difficulty_id
        TOO_LATE_MS = TOO_LATE.get(difficulty_id, 5000)
        try:
            session_id = GameSessionRepository.create_session(
                settings=settings,
                username=username,
                mode_id=mode_id,
                difficulty_id=difficulty_id,
                started_on=datetime.now(timezone.utc),
            )
        except Exception as e:
            self.logger.error(f"Error creating game session: {e}")
            raise Exception("Error creating game session: " + str(e))

        await self.new_round(sio, coneService)
        return "Game started!"
    
    async def new_round(self, sio: socketio.AsyncServer, coneService: ConeService):
        global currentRoundStartTime, currentCone, maxCones
        if (currentRoundStartTime is None and currentCone is None):
            connectedCones = coneService.get_active_cones(maxCones)
            if connectedCones is None or len(connectedCones) == 0:
                self.logger.warning("No connected cones available to start a new round.")
                raise Exception("No connected cones available to start a new round.")
            elif len(connectedCones) < maxCones:
                self.logger.warning(f"Not enough connected cones ({len(connectedCones)}) to start a new round. Required: {maxCones}.")
                raise Exception(f"Not enough connected cones ({len(connectedCones)}) to start a new round. Required: {maxCones}.")
                
            currentRoundStartTime = datetime.now(timezone.utc)
            currentCone = random.choice(connectedCones)
            self.logger.info(f"New round started. Hit cone {currentCone}!")
            await sio.emit('round_start', {'color': currentCone.color, 'round': len(roundList) + 1, "max_rounds": maxRounds})

        else:
            self.logger.warning("Cannot start a new round while another is in progress.")
    
    async def record_round(self, cone: int, sio: socketio.AsyncServer, coneService: ConeService, scoreService: ScoreService,  settings: config.Settings) -> None:

        global TOO_LATE_MS, roundList, currentRoundStartTime, currentCone, maxRounds, totalTimeMs, connectedCones
        if len(roundList) >= maxRounds:
            raise ValueError("Maximum number of rounds reached.")
        connectedCones = coneService.get_active_cones()
        coneObject = next((c for c in connectedCones if c.cone_id == cone), None)
        if coneObject is None:
            raise Exception("Cone with id " + str(cone) + " not found among connected cones.")
        if currentRoundStartTime is None or currentCone is None:
            if coneObject is None:
                raise ValueError("No round has been started. cone id: unknown")
            raise ValueError("No round has been started. id: " + str(cone))
        
        reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
        totalTimeMs += reaction_speed_ms
        if reaction_speed_ms > TOO_LATE_MS:
            round_result = RoundResult.GEMIST
        elif coneObject.cone_id != currentCone.cone_id:
            round_result = RoundResult.FOUT
        else:
            round_result = RoundResult.GOED
        
        new_round = Round(
            number=len(roundList) + 1,
            reaction_speed_ms=reaction_speed_ms,
            result=round_result,
            cone_id=coneObject.cone_id
        )
        await sio.emit('round_result', {'round': new_round.number, 'result': new_round.result})
        
        roundList.append(new_round)
        
        currentRoundStartTime = None 
        currentCone = None 
        self.logger.info(f"Round {new_round.number} recorded: {new_round}")
        if len(roundList) >= maxRounds:
            self.logger.info("Max rounds reached. Game over. rounds:")

            for r in roundList:
                self.logger.info(r)
            playerScore = scoreService.calculate_score(
                total_rounds=len(roundList), correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED), average_reaction_speed=totalTimeMs / len(roundList)
            )
            top_scores = scoreService.get_top_scores(settings, limit=3)
            gameoverStats = GameOverStats(
                total_rounds=len(roundList),
                total_time_ms=totalTimeMs,
                correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED),
                wrong_hits=sum(1 for r in roundList if r.result == RoundResult.FOUT),
                missed_hits=sum(1 for r in roundList if r.result == RoundResult.GEMIST),
                average_reaction_speed_ms=totalTimeMs / len(roundList),
                score=playerScore,
                top_scores=top_scores
            )
            # Reset game state
            roundList = []
            totalTimeMs = 0
            currentRoundStartTime = None
            currentCone = None
            for r in roundList:
                RondeRepository.create_ronde(settings, r.number, r.reaction_speed_ms, r.cone_id, r.result)
            
            GameSessionRepository.end_session(
                settings=settings,
                session_id=session_id,
                ended_on=datetime.now(timezone.utc),
                score=playerScore
            )
            player_rank = GameSessionRepository.get_player_rank(settings, session_id)
            playerScore.rank = player_rank
            gameoverStats.score = playerScore

            await sio.emit('game_over', gameoverStats.model_dump_json())
        else:
            await asyncio.sleep(1)  # brief pause before next round
            await self.new_round(sio, coneService)
