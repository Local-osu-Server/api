from contextlib import asynccontextmanager

import sqlmodel
import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine
from starlette.middleware.cors import CORSMiddleware

from v1.common.log import setup_logging
from v1.controllers.bancho import bancho_router
from v1.controllers.config import config_router
from v1.controllers.profile import profile_router
from v1.controllers.utils import utils_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.logger = setup_logging()

    # import all models for db to initialize with
    from v1.models.database.config import Config
    from v1.models.database.profile import Profile
    from v1.models.database.session import Session

    for api_v1_router in [
        config_router,
        bancho_router,
        profile_router,
        utils_router,
    ]:
        app.include_router(api_v1_router, prefix="/api/v1")

    app.state.db = create_engine(url="sqlite:///database.db", echo=False, future=True)

    sqlmodel.SQLModel.metadata.create_all(app.state.db)

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
    uvicorn.run("main:app", port=5000, reload=True)
