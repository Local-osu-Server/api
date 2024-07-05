from v1.common.game_mode import GameMode
from v1.common.ranked_status import OsuDirectRankedStatus
from httpx import AsyncClient
from pydantic import BaseModel

http_client = AsyncClient()


class DirectSearchResult(BaseModel):
    ...


async def get_direct_search(
    username: str,
    password: str,
    query: str | None = None,
    game_mode: GameMode | None = None,
    ranked_status: OsuDirectRankedStatus | None = None,
    raw_data: bool = False,
):
    params = {
        "u": username,
        "p": password,
    }

    if query:
        params["q"] = query

    if game_mode:
        params["m"] = game_mode.value  # type: ignore

    if ranked_status:
        params["r"] = ranked_status.value  # type: ignore

    response = await http_client.get(
        "https://osu.ppy.sh/web/osu-search.php",
        params=params,
    )

    if response.status_code >= 400:
        raise Exception("Error getting direct search")

    if raw_data:
        return response.content

    return DirectSearchResult()  # TODO: Parse response for osu! direct search
