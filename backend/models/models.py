import datetime
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

class MemoryGameRound(BaseModel):
    number: int
    sequence: list[int]
    user_sequence: list[int]
    result: RoundResult
    reaction_speed_ms: int

class Cone(BaseModel):
    cone_id: int
    color: str
    battery_percentage: int | None
    last_status: datetime.datetime | None

class ConeWithStatus(BaseModel):
    cone_id: int
    color: str
    battery_percentage: int
    connected: bool

class ConeDTO(BaseModel):
    cone_id: int

class ConeStatusDTO(BaseModel):
    cone_id: int
    battery_percentage: int

class ScoreEntry(BaseModel):
    username: str
    score: float | None
    place: int

class GameOverStats(BaseModel):
    total_rounds: int = 10
    total_time_ms: int
    niveau: str | None
    rounds: list[Round] | list[MemoryGameRound] = []
    correct_hits: int
    wrong_hits: int
    missed_hits: int
    average_reaction_speed_ms: float
    score: ScoreEntry
    top_scores: list[ScoreEntry] = []

class GameStartDTO(BaseModel):
    username: str
    mode_id: int
    difficulty_id: int | None
    aantal_rondes: int
    aantal_kleuren: int

class ExportDateDTO(BaseModel):
    startDate: datetime.datetime
    endDate: datetime.datetime

class StatusMessage(BaseModel):
    message: str

class Session(BaseModel):
    spelsessie_id: int
    username: str
    spelmodus_id: int
    naam: str | None
    score: int
    avg_reactietijd_ms: float
    accuracy_percent: float

class SessionData(BaseModel):
    avg_reaction_speed: float
    avg_accuracy: float
    data: list[Session]

class GameStatus(BaseModel):
    game_in_progress: bool

class GameMode(BaseModel):
    spelmodus_id: int
    naam: str
    description: str | None
    image: str | None
    icon: str | None

class Tutorial(BaseModel):
    number: int
    description: str

class ModeTutorial(BaseModel):
    image: str | None
    steps: list[Tutorial]
