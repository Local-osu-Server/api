from typing import TypedDict

from sqlalchemy.engine import Engine

from v1.errors import RepositoryProfileError, RepositorySessionError, ServerError
from v1.models.api.bancho import LoginData
from v1.repositories.profile import GetProfileResponse, ProfileRepository
from v1.repositories.session import CreateSessionResponse, SessionRepository


class LoginResponse(TypedDict):
    osu_token: str
    message: str
    profile: GetProfileResponse
    session: CreateSessionResponse


def login(
    login_data: LoginData, database_engine: Engine
) -> LoginResponse | ServerError:
    profile_repo = ProfileRepository(database_engine)
    sesion_repo = SessionRepository(database_engine)

    # check if profile already exists
    profile = profile_repo.get_by_username(login_data.username)
    if isinstance(profile, ServerError):
        if profile.error_name == RepositoryProfileError.PROFILE_NOT_FOUND:
            # create profile
            profile = profile_repo.create(login_data.username)
        else:
            return profile  # weird else case due to type hinting

    # if the server restarted, the user's session
    # would already exist in the database
    session = sesion_repo.get(profile["user_id"])

    if isinstance(session, ServerError):
        if session.error_name == RepositorySessionError.SESSION_NOT_FOUND:
            # create session
            session = sesion_repo.create(profile["user_id"])
        else:
            return session  # weird else case due to type hinting

    return {
        "osu_token": session["current_osu_token"],
        "message": "Login successful!",
        "profile": profile,
        "session": session,
    }
