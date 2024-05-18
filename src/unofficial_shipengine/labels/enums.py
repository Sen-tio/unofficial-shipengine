from enum import Enum


class ChargeEvent(Enum):
    CARRIER_DEFAULT: str = "carrier_default"
    ON_CREATION: str = "on_creation"
    ON_CARRIER_ACCEPTANCE: str = "on_carrier_acceptance"


class LabelFormat(Enum):
    PDF: str = "pdf"
    PNG: str = "png"
    ZPL: str = "zpl"


class LabelLayout(Enum):
    FOUR_BY_SIX: str = "4x6"
    LETTER: str = "letter"


class DisplayScheme(Enum):
    LABEL: str = "label"
    QR_CODE: str = "qr_code"
    LABEL_AND_QR_CODE: str = "label_and_qr_code"
    PAPERLESS: str = "paperless"
    LABEL_AND_PAPERLESS: str = "label_and_paperless"
