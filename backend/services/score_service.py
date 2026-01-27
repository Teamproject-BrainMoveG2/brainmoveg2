import logging
import config
from repositories.gamesession_repository import GameSessionRepository
from models.models import ScoreEntry
from repositories.niveau_repository import NiveauRepository
ACCURACY_WEIGHT = 0.3
REACTION_WEIGHT = 0.7
ACCURACY_MULTIPLIER = 10
MAX_REACTION_TIME_MS = 6000
SCORE_MULTIPLIER = 200
class ScoreService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("ScoreService initialized.")
    def calculate_score(self, total_rounds, correct_hits, average_reaction_speed, difficulty, divide_by=1) -> float:
        if total_rounds == 0 or average_reaction_speed <= 0:
            return 0.0
        accuracy = correct_hits / total_rounds * ACCURACY_MULTIPLIER
        score = SCORE_MULTIPLIER * ((ACCURACY_WEIGHT * accuracy) * REACTION_WEIGHT * MAX_REACTION_TIME_MS/(average_reaction_speed/divide_by))
        if difficulty == 2:
            score *= 1.1
        elif difficulty == 3:
            score *= 1.2
        return score
    
    def calculate_level(self, score: float, settings: config.Settings) -> str:
        niveau = 1
        if score >= 2500:
            niveau = 5
        elif score >= 1800:
            niveau = 4
        elif score >= 1200:
            niveau = 3
        elif score >= 600:
            niveau = 2
        else:
            niveau = 1

        niveau_text = NiveauRepository.get_niveau_by_id(settings, niveau)
        return niveau_text["name"]

    def get_top_scores(self, settings: config.Settings, mode_id: int, limit: int = 3) -> list[dict]:
        top_scores = GameSessionRepository.get_top_scores(settings, mode_id, limit=limit)
        top_scores_models = []
        if top_scores:
            for ts in top_scores:
                top_scores_models.append(ScoreEntry(
                    username=ts['username'],
                    score=ts['score'],
                    place=ts['rank']
                ))
            return top_scores_models
        return []