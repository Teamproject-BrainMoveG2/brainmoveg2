from pydantic import BaseModel
from enum import Enum

class RoundResult(str, Enum):
    GOED = "goed"    
    FOUT = "fout"    
    GEMIST = "gemist"  

class Round(BaseModel):
    number: int
    reaction_speed_ms: int
    result: RoundResult
    cone_id: int

class Cone(BaseModel):
    cone_id: int
    color: str
class ConeDTO(BaseModel):
    cone_id: int

class GameOverStats(BaseModel):
    total_rounds: int = 10
    total_time_ms: int
    correct_hits: int
    wrong_hits: int
    missed_hits: int
    average_reaction_speed_ms: float




