from typing import TypedDict

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.errors import RepositorySessionError, ServerError
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

    def delete(self, user_id: int) -> dict[str, str] | ServerError:
        with Session(self.database_engine) as session:
            statement = select(UserSession).where(
                UserSession.current_user_id == user_id
            )
            result = session.exec(statement)
            user_session: UserSession | None = result.one_or_none()

            if user_session is None:
                return ServerError(
                    error_name=RepositorySessionError.SESSION_NOT_FOUND,
                    message=f"Session with user_id {user_id} not found",
                    file_location=__file__,
                    line=ServerError.get_current_line(),
                    local_variables=locals(),
                    status_code=404,
                    in_scope_variables=dir(),
                )

            session.delete(user_session)
            session.commit()

            return {"message": "Session deleted"}

    def get(
        self, user_id: int, bypass_error_message: bool = False
    ) -> GetSessionResponse | ServerError:
        with Session(self.database_engine) as session:
            statement = select(UserSession).where(
                UserSession.current_user_id == user_id
            )
            result = session.exec(statement)
            user_session: UserSession | None = result.one_or_none()

            if user_session is None:
                return ServerError(
                    error_name=RepositorySessionError.SESSION_NOT_FOUND,
                    message=f"Session with user_id {user_id} not found",
                    file_location=__file__,
                    line=ServerError.get_current_line(),
                    local_variables=locals(),
                    status_code=404,
                    in_scope_variables=dir(),
                    log_now=False if bypass_error_message else True,
                )

            return GetSessionResponse(
                current_user_id=user_session.current_user_id,
                current_packet_queue=user_session.current_packet_queue,
                current_osu_token=user_session.current_osu_token,
            )

    # TODO: should the osu_token be the username? or should it be a uuid
    def create(self, user_id: int) -> CreateSessionResponse:
        with Session(self.database_engine) as session:
            user_session = UserSession(
                current_user_id=user_id,
                current_packet_queue=[],
                current_osu_token="ALIVE",
            )
            session.add(user_session)
            session.commit()
            session.refresh(user_session)

            return CreateSessionResponse(
                current_user_id=user_session.current_user_id,
                current_packet_queue=user_session.current_packet_queue,
                current_osu_token=user_session.current_osu_token,
            )
