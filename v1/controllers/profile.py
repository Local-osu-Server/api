from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine
from v1.models.api.bancho import LoginData

profile_router = APIRouter(prefix="/profile", tags=["Profile API"])

# TODO: on all routes, add response model to the return type
@profile_router.get("/")
async def get_profile(
    user_id: int | None = None,
    username: str | None = None,
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = usecases.profile.get(database_engine, user_id, username)
        return JSONResponse(
            status_code=200,
            content=response,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
