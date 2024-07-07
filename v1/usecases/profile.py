from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.repositories.profile import GetProfileResponse, ProfileRepository


def get(
    database_engine: Engine,
    user_id: int | None = None,
    username: str | None = None,
) -> GetProfileResponse:
    profile_repo = ProfileRepository(database_engine)

    if user_id is not None:
        response = profile_repo.get_by_user_id(user_id)
    elif username is not None:
        response = profile_repo.get_by_username(username)
    else:
        raise ValueError("Either user_id or username must be provided")

    return response
