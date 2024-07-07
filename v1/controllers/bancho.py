from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine
from v1.models.api.bancho import LoginData

bancho_router = APIRouter(prefix="/bancho", tags=["Bancho API"])


@bancho_router.post("/login")
async def login(
    login_data: LoginData,
    database_engine: Engine = Depends(get_database_engine),
):
    try:
        response = usecases.bancho.login(login_data, database_engine)
        return JSONResponse(
            status_code=200,
            content=response,
        )
    except Exception as e:
        print(e, str(e))
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
