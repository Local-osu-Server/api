from typing import TypedDict

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.models.database.session import Session as UserSession


class CreateSessionResponse(TypedDict):
    current_osu_token: str
    current_user_id: int
    current_packet_queue: list[dict]  # TODO: type this properly


class GetSessionResponse(TypedDict):
    current_osu_token: str
    current_user_id: int
    current_packet_queue: list[dict]  # TODO: type this properly


class NoSessionFoundError(Exception):
    pass


class SessionRepository:
    def __init__(self, database_engine: Engine) -> None:
        self.database_engine = database_engine

    def get(self, user_id: int) -> GetSessionResponse:
        with Session(self.database_engine) as session:
            statement = select(UserSession).where(
                UserSession.current_user_id == user_id
            )
            result = session.exec(statement)
            user_session: UserSession | None = result.one_or_none()

            if user_session is None:
                raise NoSessionFoundError(f"No session found for user id {user_id}")

            return GetSessionResponse(
                current_user_id=user_session.current_user_id,
                current_packet_queue=user_session.current_packet_queue,
                current_osu_token=user_session.current_osu_token,
            )

    # TODO: should the osu_token be the username? or should it be a uuid
    def create(self, user_id: int) -> CreateSessionResponse:
        with Session(self.database_engine) as session:
            user_session = UserSession(
                current_user_id=user_id, current_packet_queue=[], current_osu_token=""
            )
            session.add(user_session)
            session.commit()
            session.refresh(user_session)

            return CreateSessionResponse(
                current_user_id=user_session.current_user_id,
                current_packet_queue=user_session.current_packet_queue,
                current_osu_token=user_session.current_osu_token,
            )
