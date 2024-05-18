from enum import Enum


class LabelLayout(Enum):
    FOUR_BY_SIX: str = "4x6"
    LETTER: str = "letter"


class LabelFormat(Enum):
    PDF: str = "pdf"
    PNG: str = "png"
    ZPL: str = "zpl"
