import config
from repositories.gamesession_repository import GameSessionRepository
from models.models import ScoreEntry
from repositories.niveau_repository import NiveauRepository
ACCURACY_WEIGHT = 0.2
REACTION_WEIGHT = 0.8
ACCURACY_MULTIPLIER = 10
MAX_REACTION_TIME_MS = 6000
SCORE_MULTIPLIER = 200
class ScoreService:
    def calculate_score(self, total_rounds, correct_hits, average_reaction_speed, difficulty) -> float:
        if total_rounds == 0:
            return 0.0
        accuracy = correct_hits / total_rounds * ACCURACY_MULTIPLIER
        score = SCORE_MULTIPLIER * (ACCURACY_WEIGHT * accuracy + REACTION_WEIGHT * MAX_REACTION_TIME_MS/average_reaction_speed)
        if difficulty == 2:
            score *= 1.1
        elif difficulty == 3:
            score *= 1.2
        return score
    
    def calculate_level(self, score: float, settings: config.Settings) -> str:
        niveau = 0
        if score >= 1500:
            niveau = 5
        elif score >= 1200:
            niveau = 4
        elif score >= 900:
            niveau = 3
        elif score >= 600:
            niveau = 2
        elif score >= 300:
            niveau = 1
        else:
            niveau = 0

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