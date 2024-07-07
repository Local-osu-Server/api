from fastapi import Body, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine
from v1.errors import ServerError
from v1.models.api import ConfigUpdate

config_router = APIRouter(prefix="/config", tags=["config"])


@config_router.get("/")
async def get_config(database_engine: Engine = Depends(get_database_engine)):
    response = await usecases.config.get(database_engine)
    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code, content=response.to_dict()
        )
    else:
        return JSONResponse(status_code=200, content=response)


@config_router.post("/create")
async def create_config(
    config: ConfigUpdate = Body(...),
    database_engine: Engine = Depends(get_database_engine),
):
    response = await usecases.config.create(config, database_engine)
    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code, content=response.to_dict()
        )
    else:
        return JSONResponse(status_code=200, content=response)


@config_router.post("/update")
async def update_config(
    config: ConfigUpdate = Body(...),
    database_engine: Engine = Depends(get_database_engine),
):
    response = await usecases.config.update(config, database_engine)
    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code, content=response.to_dict()
        )
    else:
        return JSONResponse(status_code=200, content=response)
