from dataclasses import dataclass
from enum import Enum


class MoveType(Enum):
    HG = (0, 0)
    HM = (0, 1)
    HD = (0, 2)
    MG = (1, 0)
    MM = (1, 1)
    MD = (1, 2)
    BG = (2, 0)
    BM = (2, 1)
    BD = (2, 2)

    def all_moves():
        return [
            MoveType.HG,
            MoveType.HM,
            MoveType.HD,
            MoveType.MG,
            MoveType.MM,
            MoveType.MD,
            MoveType.BG,
            MoveType.BM,
            MoveType.BD,
        ]


@dataclass(frozen=True)
class Move:
    move_type: MoveType

    @property
    def position(self) -> tuple[int, int]:
        return self.move_type.value
