from typing import TypedDict

from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.models.database.config import Config


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
        pass

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
        with Session(self.database_engine) as session:
            statement = select(Config)
            results = session.exec(statement)
            config: Config = results.one()

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
                # TODO: Probably shouldn't be able to create a new config in the update function
                # because it would be a better implmentation to have this return an error saying there
                # is no config to update, and then returning it to the target, then the target can
                # call like /config/create and then create it 
                # and its kind of weird to have a create function in the update function
                # and its showing tight coupling between the two functions...

                if (
                    not osu_api_key
                    or not osu_daily_api_key
                    or not osu_api_v2_client_id
                    or not osu_api_v2_client_secret
                    or not osu_username
                    or not osu_password
                    or not dedicated_dev_server_domain
                ):
                    raise Exception(
                        "All config values are required to create a new config"
                    )

                kwargs = {
                    "osu_api_key": osu_api_key,
                    "osu_daily_api_key": osu_daily_api_key,
                    "osu_api_v2_client_id": osu_api_v2_client_id,
                    "osu_api_v2_client_secret": osu_api_v2_client_secret,
                    "osu_username": osu_username,
                    "osu_password": osu_password,
                    "dedicated_dev_server_domain": dedicated_dev_server_domain,
                }

                if osu_folder_path is not None:
                    kwargs["osu_folder_path"] = osu_folder_path

                if display_pp_on_leaderboard is not None:
                    kwargs["display_pp_on_leaderboard"] = display_pp_on_leaderboard

                if rank_scores_by_pp_or_score is not None:
                    kwargs["rank_scores_by_pp_or_score"] = rank_scores_by_pp_or_score

                if num_scores_seen_on_leaderboards is not None:
                    kwargs[
                        "num_scores_seen_on_leaderboards"
                    ] = num_scores_seen_on_leaderboards

                if allow_pp_from_modified_maps is not None:
                    kwargs["allow_pp_from_modified_maps"] = allow_pp_from_modified_maps

                self.create(**kwargs)

                return {"message": "Config created successfully"}

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
