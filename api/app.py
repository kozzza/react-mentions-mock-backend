import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import traceback
from datetime import datetime

import uvicorn
from decouple import config
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.elastic import Elastic
from core.schemas import RegenerateNamesAPIResponse, SearchAPIResponse

app = FastAPI(docs_url="/")

origins = [
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3000",
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

elastic = Elastic()

security = HTTPBearer()

@app.get(
    "/regenerate",
    response_model=RegenerateNamesAPIResponse,
    response_model_exclude_none=True,
)
async def regenerate_names(key: HTTPAuthorizationCredentials= Depends(security)):
    """
    Regenerates a level
    """
    try:
        if key.credentials != config("API_KEY"):
            return dict(
                status_code=403,
                message="Could not validate API KEY",
            )
        elastic.regenerate_documents()
        return dict(
            status_code=200,
            message="Success",
        )
    except Exception as e:
        return dict(
            status_code=500,
            message=str(e),
        )

@app.get(
    "/search",
    response_model=SearchAPIResponse,
    response_model_exclude_none=True,
)
async def search(query: str):
    """
    Fetches the latest level depending on the client's timezone
    """
    try:
        result = elastic.search(query)
        return dict(
            status_code=200,
            message="Success",
            data=result
        )
    except Exception as e:
        traceback.print_exc()
        return dict(
            status_code=500,
            message=str(e),
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
