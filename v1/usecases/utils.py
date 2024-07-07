from sqlalchemy.engine import Engine

import v1.adapters.osu_daily_api as osu_daily_api
from v1.adapters.osu_daily_api import RankFromPP
from v1.repositories.config import ConfigRepository


async def get_rank_from_pp(
    database_engine: Engine,
    pp: int,
) -> RankFromPP:
    config_repo = ConfigRepository(database_engine)

    config = config_repo.get()

    response = await osu_daily_api.get_rank_from_pp(
        pp,
        config["osu_daily_api_key"],
    )

    return response
