from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tags import description, tags_metadata
from routers import router

import uvicorn

app = FastAPI(
    title="Mero Search Backend Service",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8010)

