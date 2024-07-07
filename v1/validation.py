import random

import aiosu
from ossapi import Ossapi

import v1.adapters.osu_daily_api as osu_daily_api_adapter
import v1.adapters.osu_direct as osu_direct_adapter

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


class OsuApiKeyValidationError(Exception):
    ...


async def osu_api_key(api_key: str) -> dict[str, str]:
    try:
        # TODO: `aiosu.v1` should be in adapters
        async with aiosu.v1.Client(api_key) as client:
            response = await client.get_beatmap(
                beatmapset_id=random.choice(RANDOM_BEATMAP_SET_IDS)
            )
        if response:
            return {"status": "success", "message": "Osu! API V1 key is valid"}
        else:
            raise OsuApiKeyValidationError("Osu! API V1 key is invalid")
    except Exception as e:
        raise OsuApiKeyValidationError(f"Osu! API V1 key is invalid: {e}")


class OsuApiV2CredentialsValidationError(Exception):
    ...


async def osu_api_v2_credentials(client_id: int, client_secret: str) -> dict[str, str]:
    try:
        # TODO: `Ossapi` should be in adapters
        osu_api = Ossapi(client_id, client_secret)
        response = osu_api.beatmap(beatmap_id=random.choice(RANDOM_BEATMAP_IDS))
        if response:
            return {"status": "success", "message": "Osu! API V2 Credentials are valid"}
        else:
            raise OsuApiV2CredentialsValidationError(
                "Osu! API V2 Credentials are invalid"
            )
    except Exception as e:
        raise OsuApiV2CredentialsValidationError(
            f"Osu! API V2 Credentials are invalid: {e}"
        )


class OsuDailyApiKeyValidationError(Exception):
    ...


async def osu_daily_api_key(api_key: str) -> dict[str, str]:
    try:
        response = await osu_daily_api_adapter.get_rank_from_pp(1000, api_key)
        return {"status": "success", "message": "OsuDaily API key is valid"}
    except Exception as e:
        raise OsuDailyApiKeyValidationError(f"OsuDaily API key is invalid: {e}")


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
