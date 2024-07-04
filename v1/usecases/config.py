from sqlalchemy.engine import Engine

from v1.models.api import ConfigUpdate
from v1.repositories.config import ConfigRepository
from v1.usecases import validation


async def update(config: ConfigUpdate, database_engine: Engine) -> dict[str, str]:
    config_repo = ConfigRepository(database_engine)

    try:
        # Try to validate all the config values
        validation.osu_api_key(config.osu_api_key)
        validation.osu_api_v2_credentials(
            client_id=config.osu_api_v2_client_id,
            client_secret=config.osu_api_v2_client_secret,
        )
        await validation.osu_daily_api_key(config.osu_daily_api_key)
        await validation.osu_crendentials(config.osu_username, config.osu_password)
    except Exception as error:
        raise error

    response = config_repo.update(
        osu_folder_path=config.osu_folder_path,
        osu_username=config.osu_username,
        osu_password=config.osu_password,
        osu_api_v2_client_id=config.osu_api_v2_client_id,
        osu_api_v2_client_secret=config.osu_api_v2_client_secret,
        display_pp_on_leaderboard=config.display_pp_on_leaderboard,
        rank_scores_by_pp_or_score=config.rank_scores_by_pp_or_score,
        allow_pp_from_modified_maps=config.allow_pp_from_modified_maps,
        num_scores_seen_on_leaderboards=config.num_scores_seen_on_leaderboards,
        osu_api_key=config.osu_api_key,
        osu_daily_api_key=config.osu_daily_api_key,
    )
    return response
