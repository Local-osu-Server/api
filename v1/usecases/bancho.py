from typing import TypedDict

from sqlalchemy.engine import Engine

from v1.models.api.bancho import LoginData
from v1.repositories.profile import (
    GetProfileResponse,
    NoProfileFoundError,
    ProfileRepository,
)
from v1.repositories.session import (
    CreateSessionResponse,
    NoSessionFoundError,
    SessionRepository,
)


class LoginResponse(TypedDict):
    osu_token: str
    message: str
    profile: GetProfileResponse
    session: CreateSessionResponse


def login(login_data: LoginData, database_engine: Engine) -> LoginResponse:
    profile_repo = ProfileRepository(database_engine)
    sesion_repo = SessionRepository(database_engine)

    # check if profile already exists
    try:
        profile = profile_repo.get_by_username(login_data.username)
    except NoProfileFoundError:
        # create profile
        profile = profile_repo.create(login_data.username)
    except Exception as e:
        raise e

    try:
        # if the server restarted, the user's session
        # would already exist in the database
        session = sesion_repo.get(profile["user_id"])
    except NoSessionFoundError:
        # create session if doesn't exist already
        session = sesion_repo.create(profile["user_id"])
    except Exception as e:
        raise e

    return {
        "osu_token": session["current_osu_token"],
        "message": "Login successful!",
        "profile": profile,
        "session": session,
    }
