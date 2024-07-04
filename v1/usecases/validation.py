from httpx import AsyncClient
from ossapi import Ossapi, OssapiV1


class OsuApiKeyValidationError(Exception):
    ...


def osu_api_key(api_key: str) -> dict[str, str]:
    try:
        osu_api = OssapiV1(api_key)
        response = osu_api.get_beatmaps(beatmapset_id=2186776)
        if response:
            return {"status": "success", "message": "Osu! API key is valid"}
        else:
            raise OsuApiKeyValidationError("Osu! API key is invalid")
    except Exception as e:
        raise OsuApiKeyValidationError(f"Osu! API key is invalid: {e}")


class OsuApiV2CredentialsValidationError(Exception):
    ...


def osu_api_v2_credentials(client_id: int, client_secret: str) -> dict[str, str]:
    try:
        osu_api = Ossapi(client_id, client_secret)
        response = osu_api.beatmap(beatmap_id=4623482)
        if response:
            return {"status": "success", "message": "Osu! API Credentials are valid"}
        else:
            raise OsuApiV2CredentialsValidationError("Osu! API Credentials are invalid")
    except Exception as e:
        raise OsuApiV2CredentialsValidationError(
            f"Osu! API Credentials are invalid: {e}"
        )


class OsuDailyApiKeyValidationError(Exception):
    ...


async def osu_daily_api_key(api_key: str) -> dict[str, str]:
    # https://github.com/Adrriii/osudaily-api/wiki#httpsosudailynetapi
    try:
        # TODO: Potentially Make a wrapper for osudaily api
        # consider making a wrapper folder and putting this in a separate file
        # Don't know if i want to make the wrapper an object or just a bunch of functions
        async with AsyncClient() as client:
            response = await client.get(
                "https://osudaily.net/api/pp.php",
                params={
                    "k": api_key,
                    "t": "pp",
                    "v": 1000,
                },
            )
            if response.status_code == 200:
                return {"status": "success", "message": "OsuDaily API key is valid"}
            else:
                raise OsuDailyApiKeyValidationError("OsuDaily API key is invalid")
    except Exception as e:
        raise OsuDailyApiKeyValidationError(f"OsuDaily API key is invalid: {e}")


class OsuCrendentialValidationError(Exception):
    ...


async def osu_crendentials(username: str, password: str) -> dict[str, str]:
    try:
        # TODO: Potentially Make a wrapper for osu_direct
        # consider making a wrapper folder and putting this in a separate file
        # Don't know if i want to make the wrapper an object or just a bunch of functions
        async with AsyncClient() as client:
            response = await client.get(
                "https://osu.ppy.sh/web/osu-search.php",
                params={
                    "u": username,
                    "p": password,
                },
            )

            if response.status_code == 200:
                return {"status": "success", "message": "Osu! credentials are valid"}
            else:
                raise OsuCrendentialValidationError("Osu! credentials are invalid")
    except Exception as e:
        raise OsuCrendentialValidationError(f"Osu! credentials are invalid: {e}")
