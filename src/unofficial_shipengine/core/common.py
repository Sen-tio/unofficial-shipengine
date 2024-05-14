from enum import Enum
from attrs import define, field, validators


@define
class Address:
    class AddressResidentialIndicator(Enum):
        UNKNOWN: str = "unknown"
        YES: str = "yes"
        NO: str = "no"

    name: str
    phone: str
    address_line1: str
    city_locality: str
    state_province: str
    postal_code: str
    address_line2: str = None
    address_line3: str = None
    email: str = None
    company_name: str = None
    instructions: str = None
    geolocation: list[object] = None
    country_code: str = field(default="US")
    address_residential_indicator: AddressResidentialIndicator = field(
        default=AddressResidentialIndicator.UNKNOWN
    )


@define
class Error:
    error_source: str
    error_type: str
    error_code: str
    error_message: str


@define
class URL:
    href: str
    type: str = None


@define
class LabelDownload:
    href: str
    pdf: str = None
    zpl: str = None
    png: str = None


@define
class AddressValidation:

    @define
    class Message:
        code: str
        message: str
        type: str
        detail_code: str = None

    class Status(Enum):
        UNVERIFIED: str = "unverified"
        VERIFIED: str = "verified"
        WARNING: str = "warning"
        ERROR: str = "error"

    status: Status
    original_address: Address
    matched_address: Address = None
    messages: list[Message] = None


@define
class Weight:
    class Unit(Enum):
        POUND = "pound"
        OUNCE = "ounce"
        GRAM = "gram"
        KILOGRAM = "kilogram"

    value: float
    unit: Unit = field(validator=validators.in_(Unit))


@define
class Dimension:
    class Unit(Enum):
        INCH = "inch"
        CENTIMETER = "centimeter"

    length: float
    width: float
    height: float
    unit: Unit = field(default=Unit.INCH, validator=validators.in_(Unit))


@define
class Value:
    # ISO 4217: https://www.iso.org/iso-4217-currency-codes.html
    currency: str = field(default="usd")
    amount: float = field(default=0.0)


@define
class Package:

    @define
    class LabelMessages:
        reference1: str = None
        reference2: str = None
        reference3: str = None

    weight: Weight
    package_code: str = None
    dimensions: Dimension = None
    content_description: str = None
    package_id: str = None
    insurance_value: Value = None
    label_messages: LabelMessages = None
    products: list[object] = None  # TODO
    external_package_id: str = None


class ValidateAddress(Enum):
    NO_VALIDATION: str = "no_validation"
    VALIDATE_ONLY: str = "validate_only"
    VALIDATE_AND_CLEAN: str = "validate_and_clean"


def serializer(inst, field, value):
    if isinstance(value, Enum):
        return value.value
    return value
