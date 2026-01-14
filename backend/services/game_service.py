from models.models import Round, RoundResult, Cone, GameOverStats
from datetime import datetime, timezone
from fastapi import Depends
import random
import socketio
import logging
import asyncio
TOO_LATE_MS = 5000
connectedCones = [Cone(cone_id=1, color="red"), Cone(cone_id=2, color="blue"), Cone(cone_id=3, color="green"), Cone(cone_id=4, color="yellow")]
roundList = []
maxRounds = 10
currentRoundStartTime = None
currentCone = None
totalTimeMs = 0
class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("GameService initialized.")


    async def start_game(self, sio: socketio.AsyncServer) -> str:
        self.logger.info("Game started.")
        await self.new_round(sio)
        return "Game started!"
    
    async def new_round(self, sio: socketio.AsyncServer):
        global currentRoundStartTime, currentCone
        if (currentRoundStartTime is None and currentCone is None):
            currentRoundStartTime = datetime.now(timezone.utc)
            currentCone = random.choice(connectedCones)
            self.logger.info(f"New round started. Hit cone {currentCone}!")
            await sio.emit('round_start', {'color': currentCone.color, 'round': len(roundList) + 1, "max_rounds": maxRounds})

        else:
            self.logger.warning("Cannot start a new round while another is in progress.")
    
    async def record_round(self, cone: int, sio: socketio.AsyncServer) -> None:

        global TOO_LATE_MS, roundList, currentRoundStartTime, currentCone, maxRounds, totalTimeMs, connectedCones
        if len(roundList) >= maxRounds:
            raise ValueError("Maximum number of rounds reached.")
        cone = next((c for c in connectedCones if c.cone_id == cone), None)
        if currentRoundStartTime is None or currentCone is None:

            raise ValueError("No round has been started. color: " + cone.color + " id: " + str(cone.cone_id))
        
        reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
        totalTimeMs += reaction_speed_ms
        if reaction_speed_ms > TOO_LATE_MS:
            round_result = RoundResult.GEMIST
        elif cone.cone_id != currentCone.cone_id:
            round_result = RoundResult.FOUT
        else:
            round_result = RoundResult.GOED
        
        new_round = Round(
            number=len(roundList) + 1,
            reaction_speed_ms=reaction_speed_ms,
            result=round_result,
            cone_id=cone.cone_id
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
            gameoverStats = GameOverStats(
                total_rounds=len(roundList),
                total_time_ms=totalTimeMs,
                correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED),
                wrong_hits=sum(1 for r in roundList if r.result == RoundResult.FOUT),
                missed_hits=sum(1 for r in roundList if r.result == RoundResult.GEMIST),
                average_reaction_speed_ms=totalTimeMs / len(roundList)
            )
            await sio.emit('game_over', gameoverStats.model_dump_json())
        else:
            await asyncio.sleep(1)  # brief pause before next round
            await self.new_round(sio)
