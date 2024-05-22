from enum import Enum
from typing import Self, Optional, Any

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
    address_line2: str = field(default=None)
    address_line3: str = field(default=None)
    email: str = field(default=None)
    company_name: str = field(default=None)
    instructions: str = field(default=None)
    geolocation: list[object] = field(default=None)
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
    type: str = field(default=None)


@define
class LabelDownload:
    href: str
    pdf: str = field(default=None)
    zpl: str = field(default=None)
    png: str = field(default=None)


@define
class AddressValidation:
    @define
    class Message:
        code: str
        message: str
        type: str
        detail_code: str = field(default=None)

    class Status(Enum):
        UNVERIFIED: str = "unverified"
        VERIFIED: str = "verified"
        WARNING: str = "warning"
        ERROR: str = "error"

    status: Status
    original_address: Address
    matched_address: Address = field(default=None)
    messages: list[Message] = field(default=None)


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
class GenericAmount:
    amount: int = field(default=0)
    unit: str = field(default=None)


@define
class Product:

    @define
    class DangerousGood:

        class PackagingGroup(Enum):
            I: str = "i"
            II: str = "ii"
            III: str = "iii"

        class PackagingInstructionSection(Enum):
            SECTION_1: str = "section_1"
            SECTION_2: str = "section_2"
            SECTION_1A: str = "section_1a"
            SECTION_1B: str = "section_1b"

        class TransportMean(Enum):
            GROUND: str = "ground"
            WATER: str = "water"
            CARGO_AIRCRAFT_ONLY: str = "cargo_aircraft_only"
            PASSENGER_AIRCRAFT: str = "passenger_aircraft"

        class RegulationLevel(Enum):
            LIGHLTY_REGULATED: str = "lightly_regulated"
            FULLY_REGULATED: str = "fully_regulated"
            LIMITED_QUANTITIES: str = "limited_quantities"
            EXCEPTED_QUANTITY: str = "excepted_quantity"

        dangerous_amount: GenericAmount
        quantity: int = field(default=0)
        packaging_instruction: str = field(default=None)
        id_number: str = field(default=None)
        shipping_name: str = field(default=None)
        technical_name: str = field(default=None)
        product_class: str = field(default=None)
        product_class_subsidiary: str = field(default=None)
        packaging_type: str = field(default=None)
        transport_category: str = field(default=None)
        regulation_authority: str = field(default=None)
        radioactive: bool = field(default=None)
        reportable_quantity: bool = field(default=None)
        tunnel_code: str = field(default=None)
        additional_description: str = field(default=None)
        regulation_level: RegulationLevel = field(default=None)
        transport_mean: TransportMean = field(default=None)
        packaging_group: PackagingGroup = field(default=None)
        packaging_instruction_section: PackagingInstructionSection = field(default=None)

    quantity: int
    value: Value
    weight: Weight
    sku: str = field(default=None)
    sku_description: str = field(default=None)
    mid_code: str = field(default=None)
    product_url: str = field(default=None)
    vat_rate: float = field(default=None)
    unit_of_measure: str = field(default=None)
    country_of_origin: str = field(default=None)
    harmonized_tarrif_code: str = field(default=None)
    description: str = field(default=None)


@define
class Package:
    @define
    class LabelMessages:
        reference1: Optional[str] = field(default=None)
        reference2: Optional[str] = field(default=None)
        reference3: Optional[str] = field(default=None)

    weight: Weight
    package_code: Optional[str] = field(default=None)
    dimensions: Optional["Dimension"] = field(default=None)
    content_description: Optional[str] = field(default=None)
    package_id: Optional[str] = field(default=None)
    insured_value: Optional["Value"] = field(default=None)
    label_messages: Optional[LabelMessages] = field(default=None)
    products: Optional[list[Product]] = field(default=None)
    external_package_id: Optional[str] = field(default=None)
    shipment_package_id: Optional[str] = field(default=None)
    package_name: Optional[str] = field(default=None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        weight = Weight(**data.pop("weight"))
        dimensions = Dimension(**data.pop("dimensions"))
        insured_value = Value(**data.pop("insured_value"))
        label_messages = Package.LabelMessages(**data.pop("label_messages"))

        return cls(
            weight=weight,
            dimensions=dimensions,
            insured_value=insured_value,
            label_messages=label_messages,
            **data
        )
