from pydantic import BaseModel

class TestModel(BaseModel):
    device: str
    ms: str
    rssi: str
    ip: str

class StatusResponse(BaseModel):
    status: str
    data_received: TestModel

class ScoreDTO(BaseModel):
    total_rounds: int
    correct_hits: int
    average_reaction_speed: float