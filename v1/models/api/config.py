from pydantic import BaseModel


class ConfigUpdate(BaseModel):
    osu_folder_path: str
    display_pp_on_leaderboard: bool
    rank_scores_by_pp_or_score: bool
    num_scores_seen_on_leaderboards: int
    allow_pp_from_modified_maps: bool
    osu_api_key: str
    osu_daily_api_key: str
    osu_api_v2_client_id: int
    osu_api_v2_client_secret: str
    # TODO: find an alternative to needing the user's osu username and password
    osu_username: str
    osu_password: str
