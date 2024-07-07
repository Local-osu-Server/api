import random

import aiosu
from aiosu.exceptions import APIException
from ossapi import Ossapi

import v1.adapters.osu_daily_api as osu_daily_api_adapter
import v1.adapters.osu_direct as osu_direct_adapter
from v1.errors import ServerError, ValidationError

RANDOM_BEATMAP_SET_IDS = [
    2186776,
    2198714,
    2167421,
]

RANDOM_BEATMAP_IDS = [
    4623482,
    4572837,
    3989599,
]


async def osu_api_key(api_key: str) -> dict[str, str] | ServerError:
    # TODO: `aiosu.v1` should be in adapters
    try:  # special try-except block for aiosu
        async with aiosu.v1.Client(api_key) as client:
            response = await client.get_beatmap(
                beatmapset_id=random.choice(RANDOM_BEATMAP_SET_IDS)
            )
    except APIException:
        return ServerError(
            error_name=ValidationError.OSU_API_KEY_INVALID,
            message="Osu! API V1 key is invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )

    if response:
        return {"status": "success", "message": "Osu! API V1 key is valid"}
    else:
        return ServerError(
            error_name=ValidationError.OSU_API_KEY_INVALID,
            message="Osu! API V1 key is invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )


async def osu_api_v2_credentials(
    client_id: int,
    client_secret: str,
) -> dict[str, str] | ServerError:
    try:
        osu_api = Ossapi(client_id, client_secret)
        response = osu_api.beatmap(beatmap_id=random.choice(RANDOM_BEATMAP_IDS))
    except Exception:  # TODO: should be a specific exception
        return ServerError(
            error_name=ValidationError.OSU_API_V2_CREDENTIALS_INVALID,
            message="Osu! API V2 Credentials are invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )

    if response:
        return {"status": "success", "message": "Osu! API V2 Credentials are valid"}
    else:
        return ServerError(
            error_name=ValidationError.OSU_API_V2_CREDENTIALS_INVALID,
            message="Osu! API V2 Credentials are invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )


async def osu_daily_api_key(api_key: str) -> dict[str, str] | ServerError:
    response = await osu_daily_api_adapter.get_rank_from_pp(1000, api_key)

    if isinstance(response, ServerError):
        return ServerError(
            error_name=ValidationError.OSU_DAILY_API_KEY_INVALID,
            message="OsuDaily API key is invalid",
            file_location=__file__,
            line=ServerError.get_current_line(),
            in_scope_variables=dir(),
            local_variables=locals(),
            status_code=400,
        )

    return {"status": "success", "message": "OsuDaily API key is valid"}


# -----------------------------------------------------------------------------------------
class OsuCrendentialValidationError(Exception):
    ...


# TODO: I don't think we'll need crendentials
async def osu_crendentials(username: str, password: str) -> dict[str, str]:
    try:
        response = await osu_direct_adapter.get_direct_search(
            username, password, raw_data=True
        )
        return {"status": "success", "message": "Osu! credentials are valid"}
    except Exception as e:
        raise OsuCrendentialValidationError(f"Osu! credentials are invalid: {e}")
