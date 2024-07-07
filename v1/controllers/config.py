from fastapi import Body, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine
from v1.models.api import ConfigUpdate
from v1.repositories.config import NoConfigFoundError
from v1.validation import (
    OsuApiKeyValidationError,
    OsuApiV2CredentialsValidationError,
    OsuCrendentialValidationError,
    OsuDailyApiKeyValidationError,
)

config_router = APIRouter(prefix="/config", tags=["config"])


@config_router.get("/")
async def get_config(database_engine: Engine = Depends(get_database_engine)):
    try:
        response = await usecases.config.get(database_engine)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})


@config_router.post("/create")
async def create_config(
    config: ConfigUpdate = Body(...),
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = await usecases.config.create(config, database_engine)
        return JSONResponse(status_code=200, content=response)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})


@config_router.post("/update")
async def update_config(
    config: ConfigUpdate = Body(...),
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = await usecases.config.update(config, database_engine)
        return JSONResponse(status_code=200, content=response)
    except NoConfigFoundError as e:
        return JSONResponse(status_code=404, content={"error_message": str(e)})
    except OsuApiKeyValidationError as e:
        return JSONResponse(status_code=400, content={"error_message": str(e)})
    except OsuApiV2CredentialsValidationError as e:
        return JSONResponse(status_code=400, content={"error_message": str(e)})
    except OsuDailyApiKeyValidationError as e:
        return JSONResponse(status_code=400, content={"error_message": str(e)})
    except OsuCrendentialValidationError as e:
        return JSONResponse(status_code=400, content={"error_message": str(e)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error_message": str(e)})
