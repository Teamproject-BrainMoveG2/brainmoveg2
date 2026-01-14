import config
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_settings
from models.testmodels import *
from repositories.ronde_repository import RondeRepository


app = FastAPI(title="BrainMove", debug=True, description="BrainMove API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


@app.get("/")
async def hello_world(response_model=str):
    print("Hello World!")
    return 'Hello world'

@app.get("/test-db")
async def test_database_connection(settings: Annotated[config.Settings, Depends(get_settings)], response_model=StatusResponse):
    try:
        result = RondeRepository.get_ronde_by_id(settings, 1)
        if result:
            return 200
        else:
            return 500
    except Exception as e:
        return 500
    
@app.post("/ingest")
async def ingest_data(data: TestModel, response_model=StatusResponse):
    print("Data received:", data)
    return {"status": "success", "data_received": data}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True, reload_dirs=["."], host="0.0.0.0")