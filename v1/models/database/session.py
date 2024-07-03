from sqlmodel import Field, SQLModel


class Session(SQLModel, table=True):
    current_user_id: int = Field(primary_key=True)
    osu_api_v2_access_token: str
    osu_api_v2_refresh_token: str
    osu_api_v2_expires_in: int
    osu_api_v2_token_type: str
