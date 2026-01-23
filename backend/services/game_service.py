from fastapi.concurrency import run_in_threadpool
from services.mqtt_service import MQTTService
import config
from models.models import Cone, Round, RoundResult, GameOverStats, ScoreEntry, MemoryGameRound, ColorCombination
from datetime import datetime, timezone
from services.cone_service import ConeService 
from services.score_service import ScoreService
from services.buzzer_service import BuzzerService
from repositories.ronde_repository import RondeRepository
from repositories.gamesession_repository import GameSessionRepository
import random
import socketio
import logging
import asyncio

TOO_LATE = {1: 5000, 2: 4000, 3: 3000}
TOO_LATE_MS = 5000
maxRounds = 10
maxCones = 4
difficulty = None
connectedCones = []
roundList = []
currentCones = []
userCones = []
currentRoundStartTime = None
currentCone = None
totalTimeMs = 0
session_id = None
session_username = ""
session_mode_id = 0
difficulty_modifier = 0
memory_game_delay_colors = 1
game_started = False
cones = [Cone(cone_id=1, color="red", battery_percentage=None, last_status=None),
        Cone(cone_id=2, color="blue", battery_percentage=None, last_status=None),
        Cone(cone_id=3, color="green", battery_percentage=None, last_status=None),
        Cone(cone_id=4, color="yellow", battery_percentage=None, last_status=None)]
color_combinations = [
    ColorCombination(mixed="purple", base_cones=[cones[0], cones[1]]),
    ColorCombination(mixed="brown", base_cones=[cones[0], cones[2]]),
    ColorCombination(mixed="teal", base_cones=[cones[1], cones[2]]),
    ColorCombination(mixed="orange", base_cones=[cones[0], cones[3]]),
    ColorCombination(mixed="green", base_cones=[cones[1], cones[3]]),
    ColorCombination(mixed="lime", base_cones=[cones[2], cones[3]]),
]
class GameService:
    def __init__(self):
        self.logger = logging.getLogger(__name__) 
        self.logger.info("GameService initialized.")
    async def get_game_in_progress(self) -> bool:
        global game_started
        return game_started

    async def start_game(self, username: str, mode_id: int, difficulty_id: int, aantal_rondes: int, aantal_kleuren: int, sio: socketio.AsyncServer, coneService: ConeService, settings: config.Settings, buzzerService: BuzzerService, mqtt_service: MQTTService) -> str:
        global session_id, maxRounds, maxCones, difficulty, TOO_LATE_MS, session_username, session_mode_id, difficulty_modifier, game_started
        self.logger.info("Game started.")
        if len(roundList) > 0 or currentRoundStartTime is not None or currentCone is not None or game_started:
            self.logger.debug("roundList: " + str(roundList))
            self.logger.debug("currentRoundStartTime: " + str(currentRoundStartTime))
            self.logger.debug("currentCone: " + str(currentCone))
            self.logger.debug("game_started: " + str(game_started))
            self.logger.warning("Game is already in progress. Cannot start a new game.")
            raise Exception("Game is already in progress. Cannot start a new game.")
        if mode_id == 2 and aantal_kleuren < 2:
            self.logger.warning("Memory mode requires at least 2 colors.")
            raise Exception("Memory mode requires at least 2 colors.")
        if mode_id == 4 and aantal_kleuren < 4:
            self.logger.warning("Reaction mode requires at least 3 colors.")
            raise Exception("Reaction mode requires at least 3 colors.")
        maxRounds = aantal_rondes
        maxCones = aantal_kleuren
        session_username = username
        session_mode_id = mode_id
        difficulty = difficulty_id
        if difficulty_id not in [1, 2, 3]:
            if session_mode_id == 1 or session_mode_id == 2:
                raise Exception("Invalid difficulty_id for selected mode. difficulty_id: " + str(difficulty_id))
            difficulty_id = None
        if session_mode_id == 3 or session_mode_id == 4:
            difficulty_id = None
        if session_mode_id == 2:
            if difficulty_id == 1:
                difficulty_modifier = 0
            elif difficulty_id == 2:
                difficulty_modifier = 2
            elif difficulty_id == 3:
                difficulty_modifier = 4
        TOO_LATE_MS = TOO_LATE.get(difficulty_id, 5000)
        try:
            session_id = await run_in_threadpool(GameSessionRepository.create_session,
                settings=settings,
                username=username,
                mode_id=mode_id,
                difficulty_id=difficulty_id,
                started_on=datetime.now(timezone.utc),
            )
            self.logger.info(f"Game session created with ID: {session_id}")
        except Exception as e:
            self.logger.error(f"Error creating game session: {e}")
            raise Exception("Error creating game session: " + str(e))

        await self.new_round(sio, coneService, buzzerService, mqtt_service)
        game_started = True
        return "Game started!"
    
    async def stop_game(self, sio: socketio.AsyncServer, coneService: ConeService, settings: config.Settings) -> None:
        global roundList, currentRoundStartTime, currentCone, totalTimeMs, session_id, currentCones, userCones, game_started
        if not game_started and len(roundList) == 0 and currentRoundStartTime is None and currentCone is None:
            self.logger.warning("No game in progress to stop.")
            raise Exception("No game in progress to stop.")
        
        roundList = []
        totalTimeMs = 0
        currentRoundStartTime = None
        currentCone = None
        currentCones = []
        userCones = []
        game_started = False
        return
    
    async def _schedule_new_round(self, sio, coneService, buzzerService, mqtt_service):
        global game_started
        await asyncio.sleep(1)  # brief pause before next round
        # Check if game was stopped during the sleep
        if game_started:
            try:
                await self.new_round(sio, coneService, buzzerService, mqtt_service)
            except Exception as e:
                self.logger.error(f"Error starting new round in background: {e}")
    
    async def new_round(self, sio: socketio.AsyncServer, coneService: ConeService, buzzerService: BuzzerService, mqtt_service: MQTTService) -> None:
        global currentRoundStartTime, currentCone, maxCones, session_mode_id, currentCones, roundList, difficulty_modifier, color_combinations
        connectedCones = coneService.get_active_cones(maxCones)
        if connectedCones is None or len(connectedCones) == 0:
            self.logger.warning("No connected cones available to start a new round.")
            raise Exception("No connected cones available to start a new round.")
        elif len(connectedCones) < maxCones:
            self.logger.warning(f"Not enough connected cones ({len(connectedCones)}) to start a new round. Required: {maxCones}.")
            raise Exception(f"Not enough connected cones ({len(connectedCones)}) to start a new round. Required: {maxCones}.")
        
        if session_mode_id == 2:
            self.logger.info(f"Starting new round in memory mode. connected cones: {connectedCones}")
            amountOfColors = len(roundList) + 1 + difficulty_modifier
            for i in range(0, amountOfColors):
                if i == 0:
                    self.logger.debug(f"connected cones: {connectedCones}, choosing first cone for memory game")
                    randomCone = random.choice(connectedCones)
                else:
                    self.logger.debug(f"connected cones: {connectedCones}, choosing new cone excluding last cone {currentCones[i-1]}")
                    randomCone = random.choice([c for c in connectedCones if c != currentCones[i-1]])
                currentCones.append(randomCone)
                await sio.emit('round_start', {'color': randomCone.color, 'round': len(roundList) + 1})
                await asyncio.sleep(memory_game_delay_colors)

            await sio.emit('user_round_start', "Go")
            currentRoundStartTime = datetime.now(timezone.utc)
        elif session_mode_id == 4:
            self.logger.info(f"Starting new round in merge colors mode. connected cones: {connectedCones}")
            combination = random.choice(color_combinations)
            currentRoundStartTime = datetime.now(timezone.utc)
            await sio.emit('round_start', {'color': combination.mixed, 'round': len(roundList) + 1, "max_rounds": maxRounds})
            currentCones = combination.base_cones
        else:
            if (currentRoundStartTime is None and currentCone is None):
                currentCone = random.choice(connectedCones)

                # Trigger buzzer on the selected cone
                if buzzerService:
                    await run_in_threadpool(buzzerService.trigger_buzzer_for_round_start, currentCone, mqtt_service)
            
                currentRoundStartTime = datetime.now(timezone.utc)
                self.logger.info(f"New round started. Hit cone {currentCone}!")
                await sio.emit('round_start', {'color': currentCone.color, 'round': len(roundList) + 1, "max_rounds": maxRounds})

            else:
                self.logger.warning("Cannot start a new round while another is in progress.")
        
    async def record_round(self, cone: int, sio: socketio.AsyncServer, coneService: ConeService, scoreService: ScoreService,  settings: config.Settings, buzzerService: BuzzerService, mqtt_service: MQTTService) -> None:
        global TOO_LATE_MS, roundList, currentRoundStartTime, currentCone, maxRounds, totalTimeMs, connectedCones, session_username, session_id, session_mode_id, userCones, currentCones, difficulty, game_started
        connectedCones = coneService.get_active_cones()
        coneObject = next((c for c in connectedCones if c.cone_id == cone), None)
        if coneObject is None:
            raise Exception("Cone with id " + str(cone) + " not found among connected cones.")
        if currentRoundStartTime is None or currentCones is None:
            if coneObject is None:
                raise ValueError("No round has been started. cone id: unknown")
            raise ValueError("No round has been started. id: " + str(cone))
        
        if session_mode_id == 2:
            if len(userCones) < len(currentCones):
                userCones.append(coneObject)
                if len(userCones) == len(currentCones):
                    reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
                    totalTimeMs += reaction_speed_ms
                    if userCones == currentCones:
                        round_result = RoundResult.GOED
                        new_round = MemoryGameRound(
                            number=len(roundList) + 1,
                            sequence=[c.cone_id for c in currentCones],
                            user_sequence=[c.cone_id for c in userCones],
                            result=round_result,
                            reaction_speed_ms=reaction_speed_ms
                        )
                        await sio.emit('round_result', {'round': new_round.number, 'result': new_round.result})
                        roundList.append(new_round)
                        currentRoundStartTime = None 
                        currentCones = [] 
                        userCones = []
                        self.logger.info(f"Round {new_round.number} recorded: {new_round}")
                        asyncio.create_task(self._schedule_new_round(sio, coneService, buzzerService, mqtt_service))
                    else:
                        self.logger.info("Memory Game wrong, game over.")
                        self.logger.info("user: " + str(userCones) + " expected: " + str(currentCones))
                        round_result = RoundResult.FOUT
                        new_round = MemoryGameRound(
                            number=len(roundList) + 1,
                            sequence=[c.cone_id for c in currentCones],
                            user_sequence=[c.cone_id for c in userCones],
                            result=round_result,
                            reaction_speed_ms=reaction_speed_ms
                        )
                        await sio.emit('round_result', {'round': new_round.number, 'result': new_round.result})
                        roundList.append(new_round)

                        for r in roundList:
                            self.logger.info(r)
                        playerScore = ScoreEntry(
                            username=session_username,
                            score=0.0,
                            place=0
                        )
                        playerScore.score = scoreService.calculate_score(
                            total_rounds=len(roundList), correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED), average_reaction_speed=totalTimeMs / len(roundList), difficulty=difficulty
                        )
                        self.logger.info("ending session")
                        await run_in_threadpool(
                            GameSessionRepository.end_session,
                            settings=settings,
                            session_id=session_id,
                            ended_on=datetime.now(timezone.utc),
                            score=playerScore.score
                        )
                    
                        player_rank = await run_in_threadpool(GameSessionRepository.get_player_rank, settings, session_id, session_mode_id)
                        playerScore.place = player_rank["rank"]
                        if player_rank['rank'] <= 3:
                            top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=4)
                            top_scores = [ts for ts in top_scores if ts.place != player_rank['rank']][:3]
                        else:
                            top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=3)
                        if top_scores is None:
                            top_scores = []
                        niveau = scoreService.calculate_level(playerScore.score, settings)
                        gameoverStats = GameOverStats(
                            total_rounds=len(roundList),
                            total_time_ms=totalTimeMs,
                            niveau=niveau,
                            correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED),
                            wrong_hits=sum(1 for r in roundList if r.result == RoundResult.FOUT),
                            missed_hits=sum(1 for r in roundList if r.result == RoundResult.GEMIST),
                            average_reaction_speed_ms=totalTimeMs / len(roundList),
                            rounds=roundList,
                            score=playerScore,
                            top_scores=top_scores
                        )
                        gameoverStats.score = playerScore
                        await sio.emit('game_over', gameoverStats.model_dump_json())

                        rounds_to_save = roundList.copy()
                        self.stop_game(sio, coneService, settings)
                        for r in rounds_to_save:
                            await run_in_threadpool(RondeRepository.create_memory_ronde, settings, session_id, r.number, r.reaction_speed_ms, len(r.sequence), r.result)
                          

            else:
                raise ValueError("All cones for this round have already been hit. id: " + str(cone))
        elif session_mode_id == 4:
            if len(roundList) >= maxRounds:
                raise ValueError("Maximum number of rounds reached.")
            if len(userCones) < len(currentCones):
                userCones.append(coneObject)
                if len(userCones) == len(currentCones): # if round complete
                    reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
                    totalTimeMs += reaction_speed_ms
                    if sorted([c.cone_id for c in userCones]) == sorted([c.cone_id for c in currentCones]):
                        self.logger.info("Merge Colors correct!  userCones: " + str(userCones) + " currentCones: " + str(currentCones))
                        round_result = RoundResult.GOED
                    else:   
                        round_result = RoundResult.FOUT
                        self.logger.info("Merge Colors wrong. userCones: " + str(userCones) + " currentCones: " + str(currentCones))
                    new_round = Round(
                    number=len(roundList) + 1,
                    reaction_speed_ms=reaction_speed_ms,
                    result=round_result,
                    cone_id=coneObject.cone_id
                    )
                    await sio.emit('round_result', {'round': new_round.number, 'result': new_round.result})
                    
                    roundList.append(new_round)
                    
                    currentRoundStartTime = None 
                    currentCones = []
                    userCones = []

                    if len(roundList) >= maxRounds: #game over rounds reached
                        self.logger.info("Max rounds reached. Game over. rounds:")

                        for r in roundList:
                            self.logger.debug(r)
                        playerScore = ScoreEntry(
                            username=session_username,
                            score=0.0,
                            place=0
                        )
                        playerScore.score = scoreService.calculate_score(
                            total_rounds=len(roundList), correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED), average_reaction_speed=totalTimeMs / len(roundList), difficulty=difficulty
                        )
                        self.logger.info("ending session")
                        await run_in_threadpool(
                            GameSessionRepository.end_session,
                            settings=settings,
                            session_id=session_id,
                            ended_on=datetime.now(timezone.utc),
                            score=playerScore.score
                        )
                    
                        player_rank = await run_in_threadpool(GameSessionRepository.get_player_rank, settings, session_id, session_mode_id)
                        playerScore.place = player_rank["rank"]
                        if player_rank['rank'] <= 3:
                            top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=4)
                            top_scores = [ts for ts in top_scores if ts.place != player_rank['rank']][:3]
                        else:
                            top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=3)
                        if top_scores is None:
                            top_scores = []
                        niveau = scoreService.calculate_level(playerScore.score, settings)
                        gameoverStats = GameOverStats(
                            total_rounds=len(roundList),
                            total_time_ms=totalTimeMs,
                            niveau=niveau,
                            correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED),
                            wrong_hits=sum(1 for r in roundList if r.result == RoundResult.FOUT),
                            missed_hits=sum(1 for r in roundList if r.result == RoundResult.GEMIST),
                            average_reaction_speed_ms=totalTimeMs / len(roundList),
                            rounds=roundList,
                            score=playerScore,
                            top_scores=top_scores
                        )
                        gameoverStats.score = playerScore
                        await sio.emit('game_over', gameoverStats.model_dump_json())

                        rounds_to_save = roundList.copy()
                        self.stop_game(sio, coneService, settings)
                        for r in rounds_to_save:
                            await run_in_threadpool(RondeRepository.create_ronde, settings, session_id, r.number, r.reaction_speed_ms, None, r.result)
                    else:
                        self.logger.info("Merge Colors round complete, scheduling new round.")
                        asyncio.create_task(self._schedule_new_round(sio, coneService, buzzerService, mqtt_service))

        else:
            self.logger.debug(f"session_id {session_id}")
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
            
            self.logger.info(f"Recording hit for cone {cone} in session {session_id}.")
            reaction_speed_ms = int((datetime.now(timezone.utc) - currentRoundStartTime).total_seconds() * 1000)
            totalTimeMs += reaction_speed_ms
            if reaction_speed_ms > TOO_LATE_MS and session_mode_id != 3:
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
                    self.logger.debug(r)
                playerScore = ScoreEntry(
                    username=session_username,
                    score=0.0,
                    place=0
                )
                playerScore.score = scoreService.calculate_score(
                    total_rounds=len(roundList), correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED), average_reaction_speed=totalTimeMs / len(roundList), difficulty=difficulty
                )
                self.logger.info("session id: " + str(session_id))

                await run_in_threadpool(
                    GameSessionRepository.end_session,
                    settings=settings,
                    session_id=session_id,
                    ended_on=datetime.now(timezone.utc),
                    score=playerScore.score
                )
                self.logger.info("session id: " + str(session_id))
                


                self.logger.info("session id: " + str(session_id))
                player_rank = await run_in_threadpool(GameSessionRepository.get_player_rank, settings, session_id, session_mode_id)
                self.logger.info("player rank: " + str(player_rank))
                playerScore.place = player_rank["rank"]
                try:
                    if player_rank['rank'] <= 3:
                        top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=4)
                        top_scores = [ts for ts in top_scores if ts.place != player_rank['rank']][:3]
                    else:
                        top_scores = await run_in_threadpool(scoreService.get_top_scores, settings, session_mode_id, limit=3)
                    if top_scores is None:
                        top_scores = []
                except Exception as e:
                    top_scores = []
                    self.logger.error(f"Error retrieving top scores: {e}")
                    
                niveau = scoreService.calculate_level(playerScore.score, settings)
                gameoverStats = GameOverStats(
                    total_rounds=len(roundList),
                    total_time_ms=totalTimeMs,
                    niveau=niveau,
                    correct_hits=sum(1 for r in roundList if r.result == RoundResult.GOED),
                    wrong_hits=sum(1 for r in roundList if r.result == RoundResult.FOUT),
                    missed_hits=sum(1 for r in roundList if r.result == RoundResult.GEMIST),
                    average_reaction_speed_ms=totalTimeMs / len(roundList),
                    rounds=roundList,
                    score=playerScore,
                    top_scores=top_scores
                )
                gameoverStats.score = playerScore
                await sio.emit('game_over', gameoverStats.model_dump_json())

                rounds_to_save = roundList.copy()
                self.stop_game(sio, coneService, settings)
                for r in rounds_to_save:
                    await run_in_threadpool(RondeRepository.create_ronde, settings, session_id, r.number, r.reaction_speed_ms, r.cone_id, r.result)
            else:
                asyncio.create_task(self._schedule_new_round(sio, coneService, buzzerService, mqtt_service))