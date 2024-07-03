from sqlmodel import Field, SQLModel


class Config(SQLModel, table=True):
    osu_folder_path: str = Field(primary_key=True)
    display_pp_on_leaderboard: bool = Field(default=True)
    rank_scores_by_pp_or_score: bool = Field(default=False)
    num_scores_seen_on_leaderboards: int = Field(default=100, ge=0, le=100)
    allow_pp_from_modified_maps: bool = Field(default=True)
    osu_api_key: str | None = Field(default=None)
    osu_daily_api_key: str
    osu_api_v2_client_id: int
    osu_api_v2_client_secret: str
    # TODO: find an alternative to needing the user's osu username and password
    osu_username: str | None = Field(default=None)
    osu_password: str | None = Field(default=None)
