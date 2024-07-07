from typing import TypedDict

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.models.database.config import Config

NO_CONFIG_ERROR_MESSAGES = [
    "No row was found when one was required",
    "Expecting value: line 1 column 1 (char 0)",
]


class NoConfigFoundError(Exception):
    ...


class GetConfigResponse(TypedDict):
    osu_folder_path: str
    display_pp_on_leaderboard: bool
    rank_scores_by_pp_or_score: bool
    num_scores_seen_on_leaderboards: int
    allow_pp_from_modified_maps: bool
    osu_api_key: str | None
    osu_daily_api_key: str
    osu_api_v2_client_id: int
    osu_api_v2_client_secret: str
    osu_username: str | None
    osu_password: str | None
    dedicated_dev_server_domain: str


class ConfigRepository:
    def __init__(self, database_engine: Engine) -> None:
        self.database_engine = database_engine

    def create(
        self,
        osu_api_key: str,
        osu_daily_api_key: str,
        osu_api_v2_client_id: int,
        osu_api_v2_client_secret: str,
        osu_username: str,
        osu_password: str,
        dedicated_dev_server_domain: str,
        osu_folder_path: str = "",
        display_pp_on_leaderboard: bool = True,
        rank_scores_by_pp_or_score: bool = False,
        num_scores_seen_on_leaderboards: int = 100,
        allow_pp_from_modified_maps: bool = True,
    ) -> dict[str, str]:
        with Session(self.database_engine) as session:
            config = Config(
                osu_folder_path=osu_folder_path,
                display_pp_on_leaderboard=display_pp_on_leaderboard,
                rank_scores_by_pp_or_score=rank_scores_by_pp_or_score,
                num_scores_seen_on_leaderboards=num_scores_seen_on_leaderboards,
                allow_pp_from_modified_maps=allow_pp_from_modified_maps,
                osu_api_key=osu_api_key,
                osu_daily_api_key=osu_daily_api_key,
                osu_api_v2_client_id=osu_api_v2_client_id,
                osu_api_v2_client_secret=osu_api_v2_client_secret,
                osu_username=osu_username,
                osu_password=osu_password,
                dedicated_dev_server_domain=dedicated_dev_server_domain,
            )
            session.add(config)
            session.commit()

        return {"message": "Config created successfully"}

    def get(self) -> GetConfigResponse:
        # TODO: better error handling
        try:  # try to get the config
            with Session(self.database_engine) as session:
                statement = select(Config)
                results = session.exec(statement)
                config: Config = results.one()
        except Exception as e:
            exception_message = str(e)
            if exception_message in NO_CONFIG_ERROR_MESSAGES:
                raise NoConfigFoundError("No config found")

        return {
            "osu_folder_path": config.osu_folder_path,
            "display_pp_on_leaderboard": config.display_pp_on_leaderboard,
            "rank_scores_by_pp_or_score": config.rank_scores_by_pp_or_score,
            "num_scores_seen_on_leaderboards": config.num_scores_seen_on_leaderboards,
            "allow_pp_from_modified_maps": config.allow_pp_from_modified_maps,
            "osu_api_key": config.osu_api_key,
            "osu_daily_api_key": config.osu_daily_api_key,
            "osu_api_v2_client_id": config.osu_api_v2_client_id,
            "osu_api_v2_client_secret": config.osu_api_v2_client_secret,
            "osu_username": config.osu_username,
            "osu_password": config.osu_password,
            "dedicated_dev_server_domain": config.dedicated_dev_server_domain,
        }

    def update(
        self,
        osu_folder_path: str | None,
        display_pp_on_leaderboard: bool | None,
        rank_scores_by_pp_or_score: bool | None,
        num_scores_seen_on_leaderboards: int | None,
        allow_pp_from_modified_maps: bool | None,
        osu_api_key: str | None,
        osu_daily_api_key: str | None,
        osu_api_v2_client_id: int | None,
        osu_api_v2_client_secret: str | None,
        osu_username: str | None,
        osu_password: str | None,
        dedicated_dev_server_domain: str | None,
    ) -> dict[str, str]:
        with Session(self.database_engine) as session:
            statement = select(Config)
            results = session.exec(statement)
            config: Config | None = results.one_or_none()

            if not config:
                raise NoConfigFoundError("No config found to update")

            if osu_folder_path:
                config.osu_folder_path = osu_folder_path

            if display_pp_on_leaderboard:
                config.display_pp_on_leaderboard = display_pp_on_leaderboard

            if rank_scores_by_pp_or_score:
                config.rank_scores_by_pp_or_score = rank_scores_by_pp_or_score

            if num_scores_seen_on_leaderboards:
                config.num_scores_seen_on_leaderboards = num_scores_seen_on_leaderboards

            if allow_pp_from_modified_maps:
                config.allow_pp_from_modified_maps = allow_pp_from_modified_maps

            if osu_api_key:
                config.osu_api_key = osu_api_key

            if osu_daily_api_key:
                config.osu_daily_api_key = osu_daily_api_key

            if osu_api_v2_client_id:
                config.osu_api_v2_client_id = osu_api_v2_client_id

            if osu_api_v2_client_secret:
                config.osu_api_v2_client_secret = osu_api_v2_client_secret

            if osu_username:
                config.osu_username = osu_username

            if osu_password:
                config.osu_password = osu_password

            if dedicated_dev_server_domain:
                config.dedicated_dev_server_domain = dedicated_dev_server_domain

            session.add(config)
            session.commit()

        return {"message": "Config updated successfully"}
