import os
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_sio, get_settings
from models.testmodels import *
from models.models import *
from routers import cones, games, modes, data
import logging
import socketio
from services.mqtt_service import MQTTService
from services.score_service import ScoreService

os.makedirs('./logs', exist_ok=True)
logging.root.handlers.clear()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(console_formatter)

file_handler = logging.FileHandler('./logs/brainmove.log')
file_handler.setLevel(logging.WARNING)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


app = FastAPI(title="BrainMove", debug=True, description="BrainMove API", logger=logger)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi', logger=True)
sio_app = socketio.ASGIApp(sio, app)
app.state.sio = sio
app.include_router(router=games.router, dependencies=[Depends(get_sio)])
app.include_router(router=modes.router, dependencies=[Depends(get_sio)])
app.include_router(router=cones.router, dependencies=[Depends(get_sio)])
app.include_router(router=data.router, dependencies=[Depends(get_sio)])
app.mount("/socket.io", sio_app)

settings = get_settings()

mqtt = MQTTService(settings.mqtt_broker, settings.mqtt_port, settings.mqtt_username, settings.mqtt_password)
mqtt.connect()
app.state.mqtt = mqtt


@app.get("/", response_model=str)
async def hello_world():
    logger.info("Hello World endpoint called.")
    sio.emit('message', {'data': 'Hello, World!'})
    return 'Hello world'

@app.post("/ingest")
async def ingest_data(data: TestModel, response_model=StatusResponse):
    print("Data received:", data)
    return {"status": "success", "data_received": data}

@app.post("/test-score")
async def test_score_endpoint(score: ScoreDTO, score_service: ScoreService = Depends(ScoreService)):
    logger.info(f"Test score received: {score}")
    calculated_score = score_service.calculate_score(
        total_rounds=score.total_rounds,
        correct_hits=score.correct_hits,
        average_reaction_speed=score.average_reaction_speed,
        difficulty=score.difficulty,
        divide_by=score.divide_by
    )
    logger.info(f"Calculated score: {calculated_score}")

    return {"message": "Score received", "score": calculated_score}
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("B2F_client_connected", {"client_id": sid}, to=sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:sio_app", port=8000, reload=True, reload_dirs=["."], host="0.0.0.0")