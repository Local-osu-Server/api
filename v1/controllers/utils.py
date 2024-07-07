from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine

utils_router = APIRouter(prefix="/utils", tags=["Utilities API"])

# TODO: Probably should rethink about the location of this route
@utils_router.get("/get_rank_from_pp")
async def get_profile(
    pp: int,
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = await usecases.utils.get_rank_from_pp(database_engine, pp)
        return JSONResponse(
            status_code=200,
            content=response,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
