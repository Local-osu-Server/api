from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.engine import Engine

from v1 import usecases
from v1.common.database import get_database_engine
from v1.errors import ServerError
from v1.models.api.bancho import LoginData, LogoutData

bancho_router = APIRouter(prefix="/bancho", tags=["Bancho API"])


@bancho_router.post("/login")
async def login(
    login_data: LoginData,
    database_engine: Engine = Depends(get_database_engine),
):
    response = usecases.bancho.login(login_data, database_engine)

    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(
        status_code=200,
        content=response,
    )


@bancho_router.post("/logout")
async def logout(
    logout_data: LogoutData,
    database_engine: Engine = Depends(get_database_engine),
):
    response = usecases.bancho.logout(logout_data.user_id, database_engine)

    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(
        status_code=200,
        content=response,
    )


@bancho_router.get("/session")
async def get_session(
    user_id: int,
    database_engine: Engine = Depends(get_database_engine),
):
    response = usecases.bancho.get_session(user_id, database_engine)

    if isinstance(response, ServerError):
        return JSONResponse(
            status_code=response.status_code,
            content=response.to_dict(),
        )

    return JSONResponse(
        status_code=200,
        content=response,
    )
