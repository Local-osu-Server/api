# https://github.com/Adrriii/osudaily-api/wiki#httpsosudailynetapi

from httpx import AsyncClient
from pydantic import BaseModel

http_client = AsyncClient()

# TODO: Consider using an object to store the osu!daily api key


class RankFromPP(BaseModel):
    rank: int
    pp: float


async def get_rank_from_pp(
    pp: float,
    api_key: str,
) -> RankFromPP:
    response = await http_client.get(
        "https://osudaily.net/api/pp.php",
        params={
            "k": api_key,
            "t": "pp",
            "v": pp,
        },
    )

    if response.status_code >= 400:
        raise Exception("Error getting rank from pp")

    return RankFromPP(
        rank=response.json()["rank"],
        pp=pp,
    )
