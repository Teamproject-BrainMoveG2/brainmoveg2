from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="BrainMove", debug=True, description="BrainMove API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],)


@app.get("/")
async def hello_world(response_model=str):
    print("Hello World!")
    return 'Hello world'



if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8000, reload=True, reload_dirs=["."])