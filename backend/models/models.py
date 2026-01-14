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
    color: str = "red"




