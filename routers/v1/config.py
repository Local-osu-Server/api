from fastapi import Body, Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

import usecases
from api_models.version_one import ConfigUpdate

config_router = APIRouter(prefix="/config", tags=["config"])

# TODO: format it in the js file on the frontend
def get_configuration(
    from_onboarding: bool = False, configuration: dict = Body(...)
) -> ConfigUpdate:
    if from_onboarding:
        return ConfigUpdate(
            osu_path=configuration["osu_path"],
            display_pp_on_leaderboard=configuration["display_pp_on_leaderboard"]
            == "on",
            rank_scores_by_pp_or_score=configuration["rank_scores_by_pp_or_score"]
            == "on",
            num_scores_seen_on_leaderboards=int(
                configuration["num_scores_seen_on_leaderboards"]
            ),
            allow_pp_from_modified_maps=configuration["allow_pp_from_modified_maps"]
            == "on",
            osu_api_key=configuration["osu_api_key"],
            osu_daily_api_key=configuration["osu_daily_api_key"],
            osu_api_v2_key=configuration["osu_api_v2_key"],
            osu_username=configuration["osu_username"],
            osu_password=configuration["osu_password"],
            mitmproxy=None,
            cloudflare=None,
            developer=None,
        )
    else:
        return ConfigUpdate(**configuration)


@config_router.post("/update")
async def update_config(
    config: ConfigUpdate = Depends(get_configuration),
):
    try:
        usecases.v1.config.update()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
