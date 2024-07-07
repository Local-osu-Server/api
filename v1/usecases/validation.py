import v1.validation as validation
from v1.errors import ServerError


async def osu_api_key(api_key: str) -> dict[str, str] | ServerError:
    response = await validation.osu_api_key(api_key)
    if isinstance(response, ServerError):
        return response
    else:
        return {"status": "success", "message": "Osu! API key is valid"}


async def osu_api_v2_credentials(
    client_id: int, client_secret: str
) -> dict[str, str] | ServerError:
    response = await validation.osu_api_v2_credentials(client_id, client_secret)
    if isinstance(response, ServerError):
        return response
    else:
        return {"status": "success", "message": "Osu! API Credentials are valid"}


async def osu_daily_api_key(api_key: str) -> dict[str, str] | ServerError:
    response = await validation.osu_daily_api_key(api_key)
    if isinstance(response, ServerError):
        return response
    else:
        return {"status": "success", "message": "OsuDaily API key is valid"}


async def osu_crendentials(username: str, password: str) -> dict[str, str]:
    try:
        # TODO: remove this function because we shouldn't need the user's osu! credentials
        # remove everything that has to do with this method
        # await validation.osu_crendentials(username, password)
        return {"status": "success", "message": "Osu! credentials are valid"}
    except Exception as e:
        raise e
