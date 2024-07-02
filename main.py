from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import config
from routers.v1 import config_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.include_router(config_router, prefix="/api/v1")

    yield


app = FastAPI(lifespan=lifespan)

# TODO: understand this solution, https://github.com/tiangolo/fastapi/issues/1663
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=config.PORT, reload=True)
