from sqlalchemy.engine import Engine
from sqlmodel import Session, select

from v1.models.database.config import Config


class ConfigRepository:
    def __init__(self, database_engine: Engine) -> None:
        self.database_engine = database_engine
        pass

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
    ) -> dict[str, str]:
        try:
            with Session(self.database_engine) as session:
                statement = select(Config)
                results = session.exec(statement)
                config: Config = results.one()

                if osu_folder_path:
                    config.osu_folder_path = osu_folder_path

                if display_pp_on_leaderboard:
                    config.display_pp_on_leaderboard = display_pp_on_leaderboard

                if rank_scores_by_pp_or_score:
                    config.rank_scores_by_pp_or_score = rank_scores_by_pp_or_score

                if num_scores_seen_on_leaderboards:
                    config.num_scores_seen_on_leaderboards = (
                        num_scores_seen_on_leaderboards
                    )

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

                session.add(config)
                session.commit()
        except Exception as e:
            return {"message": f"Error updating config: {e}"}

        return {"message": "Config updated successfully"}
