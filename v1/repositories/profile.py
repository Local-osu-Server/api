from typing import TypedDict

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.models.database.profile import Profile


class GetProfileResponse(TypedDict):
    user_id: int
    username: str
    accuracy: float
    play_count: int
    total_score: int
    pp: int


class CreateProfileResponse(GetProfileResponse):
    ...


class NoProfileFoundError(Exception):
    ...


class ProfileRepository:
    def __init__(self, database_engine: Engine) -> None:
        self.database_engine = database_engine

    def get_by_user_id(self, user_id: int) -> GetProfileResponse:
        with Session(self.database_engine) as session:
            statement = select(Profile).where(Profile.user_id == user_id)
            result = session.exec(statement)
            profile: Profile | None = result.one_or_none()

            if profile is None:
                raise NoProfileFoundError(f"Profile with user id {user_id} not found")

            return GetProfileResponse(
                user_id=profile.user_id,
                username=profile.username,
                accuracy=profile.accuracy,
                play_count=profile.play_count,
                total_score=profile.total_score,
                pp=profile.pp,
            )

    def get_by_username(self, username: str) -> GetProfileResponse:
        with Session(self.database_engine) as session:
            statement = select(Profile).where(Profile.username == username)
            result = session.exec(statement)
            profile: Profile | None = result.one_or_none()

            if profile is None:
                # TODO: create a custom exception for this
                raise NoProfileFoundError(f"Profile with username {username} not found")

            return GetProfileResponse(
                user_id=profile.user_id,
                username=profile.username,
                accuracy=profile.accuracy,
                play_count=profile.play_count,
                total_score=profile.total_score,
                pp=profile.pp,
            )

    def create(self, username: str) -> GetProfileResponse:
        with Session(self.database_engine) as session:
            profile = Profile(username=username)  # type: ignore
            session.add(profile)
            session.commit()
            session.refresh(profile)

            return CreateProfileResponse(
                user_id=profile.user_id,
                username=profile.username,
                accuracy=profile.accuracy,
                play_count=profile.play_count,
                total_score=profile.total_score,
                pp=profile.pp,
            )
