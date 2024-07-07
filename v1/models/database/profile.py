from sqlmodel import Field, SQLModel


class Profile(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    username: str
    accuracy: float = Field(default=0.0)
    play_count: int = Field(default=0)
    total_score: int = Field(default=0)
    pp: int = Field(default=0)
