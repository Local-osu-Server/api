# https://github.com/Adrriii/osudaily-api/wiki#httpsosudailynetapi

import subprocess
from typing import TypedDict

import orjson
from httpx import AsyncClient

from v1.common.log import LogTypes, log
from v1.errors import OsuDailyAPIError, ServerError

http_client = AsyncClient()

# TODO: Consider using an object to store the osu!daily api key


class RankFromPP(TypedDict):
    rank: int
    pp: float


# use subprocess & curl because when using mitmproxy
# we get a CERTIFICATE_VERIFY_FAILED error :(
# TODO: find a way like i did with *.ppy.sh to have mitmproxy avoid osudaily.net
async def get_rank_from_pp(
    pp: float,
    api_key: str,
) -> RankFromPP | ServerError:
    # TODO: better error handling
    curl_command = f'curl "https://osudaily.net/api/pp.php?k={api_key}&t=pp&v={pp}"'
    process = subprocess.run(curl_command, text=True, capture_output=True)
    response = orjson.loads(process.stdout)

    if response is None:
        log(
            "Getting rank from pp, response was None, returning rank 0",
            LogTypes.WARNING,
        )
        return RankFromPP(
            rank=0,
            pp=pp,
        )

    if "error" in response:
        return ServerError(
            error_name=OsuDailyAPIError.OSU_DAILY_API_KEY_INVALID,
            message="OsuDaily API key is invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )

    return RankFromPP(
        rank=response["rank"],
        pp=pp,
    )

    """
    try:
        response = await http_client.get(
            "https://osudaily.net/api/pp.php",
            params={
                "k": api_key,
                "t": "pp",
                "v": pp,
            },
        )
    except Exception as e:
        print
        raise Exception(f"Error getting rank from pp: {e}")
    
    

    if response.status_code >= 400:
        raise Exception("Error getting rank from pp")

    return RankFromPP(
        rank=response.json()["rank"],
        pp=pp,
    )
    """
