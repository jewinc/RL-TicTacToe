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
    
    def __str__(self):
        return f"{self.name}"

    @classmethod
    def H_row(cls):
        return [cls.HG, cls.HM, cls.HD]

    @classmethod
    def M_row(cls):
        return [cls.MG, cls.MM, cls.MD]

    @classmethod
    def B_row(cls):
        return [cls.BG, cls.BM, cls.BD]

    @classmethod
    def G_col(cls):
        return [cls.HG, cls.MG, cls.BG]

    @classmethod
    def M_col(cls):
        return [cls.HM, cls.MM, cls.BM]

    @classmethod
    def D_col(cls):
        return [cls.HD, cls.MD, cls.BD]

    @classmethod
    def H_diag(cls):
        return [cls.HG, cls.MM, cls.BD]

    @classmethod
    def D_diag(cls):
        return [cls.HD, cls.MM, cls.BG]

    @classmethod
    def all_moves(cls):
        return list(cls)
    
    @classmethod
    def from_str(cls, move_str:str):
        if move_str not in cls.__members__:
            return None
        return cls[move_str]
