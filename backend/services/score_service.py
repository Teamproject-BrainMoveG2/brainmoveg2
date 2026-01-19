

ACCURACY_WEIGHT = 0.3
ACCURACY_MULTIPLIER = 10
MAX_REACTION_TIME_MS = 5000
SCORE_MULTIPLIER = 100
class ScoreService:
    def calculate_score(self, total_rounds, correct_hits, average_reaction_speed) -> float:
        if total_rounds == 0:
            return 0.0
        accuracy = correct_hits / total_rounds * ACCURACY_MULTIPLIER
        score = SCORE_MULTIPLIER * (ACCURACY_WEIGHT * accuracy + (1 - ACCURACY_WEIGHT) * MAX_REACTION_TIME_MS/average_reaction_speed)
        return score