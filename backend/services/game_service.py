from models.models import Round, RoundResult, Cone
from datetime import datetime, timezone
from fastapi import Depends
import random
import socketio
import logging
connectedCones = [Cone(cone_id=1, color="red"), Cone(cone_id=2, color="blue"), Cone(cone_id=3, color="green"), Cone(cone_id=4, color="yellow")]
roundList = []
currentRoundStartTime = None
currentCone = None 
class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("GameService initialized.")


    async def start_game(self, sio: socketio.AsyncServer) -> str:
        self.logger.info("Game started.")
        await self.new_round()
        await sio.emit('round_start', {'color': currentCone.color, 'round': len(roundList) + 1})
        return "Game started!"
    
    async def new_round(self):
        global currentRoundStartTime, currentCone
        if (currentRoundStartTime is None and currentCone is None):
            currentRoundStartTime = datetime.now(timezone.utc)
            currentCone = random.choice(connectedCones)
            self.logger.info(f"New round started. Hit cone {currentCone}!")
        else:
            self.logger.warning("Cannot start a new round while another is in progress.")
    
    async def record_round(self,cone: Cone,sio: socketio.AsyncServer) -> None:
        global roundList, currentRoundStartTime, currentCone
        if currentRoundStartTime is None or currentCone is None:
            raise ValueError("No round has been started.")
        
        reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
        
        if cone.cone_id != currentCone.cone_id:
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
        await self.new_round()
        await sio.emit('round_start', {'color': currentCone.color, 'round': len(roundList) + 1})