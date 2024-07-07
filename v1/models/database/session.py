from sqlmodel import JSON, Column, Field, SQLModel


class Session(SQLModel, table=True):
    current_user_id: int = Field(primary_key=True)
    current_osu_token: str

    # list of packets (in json format)
    # TODO: replace dict with Packet typedict
    current_packet_queue: list[dict] = Field(sa_column=Column(JSON))

    class Config:
        arbitrary_types_allowed = True
