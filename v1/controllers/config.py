from fastapi import Body, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.models.api import ConfigUpdate

config_router = APIRouter(prefix="/config", tags=["config"])


def get_database_engine(request: Request):
    return request.app.state.db


@config_router.post("/update")
async def update_config(
    config: ConfigUpdate = Body(...),
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = usecases.config.update(config, database_engine)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
