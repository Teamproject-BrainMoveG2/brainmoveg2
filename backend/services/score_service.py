import config
from repositories.gamesession_repository import GameSessionRepository
from models.models import ScoreEntry
ACCURACY_WEIGHT = 0.2
REACTION_WEIGHT = 0.8
ACCURACY_MULTIPLIER = 10
MAX_REACTION_TIME_MS = 6000
SCORE_MULTIPLIER = 200
class ScoreService:
    def calculate_score(self, total_rounds, correct_hits, average_reaction_speed) -> float:
        if total_rounds == 0:
            return 0.0
        accuracy = correct_hits / total_rounds * ACCURACY_MULTIPLIER
        score = SCORE_MULTIPLIER * (ACCURACY_WEIGHT * accuracy + REACTION_WEIGHT * MAX_REACTION_TIME_MS/average_reaction_speed)
        return score
    def get_top_scores(self, settings: config.Settings, limit: int = 3) -> list[dict]:
        top_scores = GameSessionRepository.get_top_scores(settings, limit=limit)
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