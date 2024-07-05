from enum import IntEnum


class OsuDirectRankedStatus(IntEnum):
    Ranked = 0
    Pending = 2
    Qualified = 3
    All_Ranked_Statuses = 4
    Graveyard = 5
    Played_Before = 7
    Loved = 8


class RankedStatus(IntEnum):
    NotSubmitted = -1
    Pending = 0
    UpdateAvailable = 1
    Ranked = 2
    Approved = 3
    Qualified = 4
    Loved = 5

    """
    def to_osu_direct(self) -> OsuDirectRankedStatus:
        return {
            self.NotSubmitted: OsuDirectRankedStatus.Graveyard,
            self.Pending: OsuDirectRankedStatus.Pending,
            self.UpdateAvailable: OsuDirectRankedStatus.Pending,
            self.Ranked: OsuDirectRankedStatus.Ranked,
            self.Approved: OsuDirectRankedStatus.Qualified,
            self.Qualified: OsuDirectRankedStatus.Qualified,
            self.Loved: OsuDirectRankedStatus.Loved,
        }[self]

    @classmethod
    def from_osu_direct(
        cls, osu_direct_status: OsuDirectRankedStatus
    ) -> "RankedStatus":
        # osu_direct_status = 4 is all ranked status
        try:
            return {
                OsuDirectRankedStatus.Ranked: cls.Ranked,
                OsuDirectRankedStatus.Pending: cls.Pending,
                OsuDirectRankedStatus.Qualified: cls.Qualified,
                OsuDirectRankedStatus.Graveyard: cls.Pending,
                OsuDirectRankedStatus.Played_Before: cls.Ranked,
                OsuDirectRankedStatus.Loved: cls.Loved,
            }[osu_direct_status]
        except KeyError:
            raise ValueError(f"Invalid osu!direct status: {osu_direct_status}")
    """