import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Query, Body
import uvicorn
from src.api.hotels import router as router_hotels
from src.config import settings 


print(
    f"DB_NAME: {settings.DB_NAME}"
)


app = FastAPI()

app.include_router(router_hotels)
                



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)