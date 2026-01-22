from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_sio, get_settings
from models.testmodels import *
from models.models import *
from routers import cones, games, modes, data
import logging
import socketio
from services.mqtt_service import MQTTService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
logger.info("MQTT Service connected and assigned to app state.")
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

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit("B2F_client_connected", {"client_id": sid}, to=sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:sio_app", port=8000, reload=True, reload_dirs=["."], host="0.0.0.0")