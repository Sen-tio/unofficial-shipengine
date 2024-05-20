from enum import Enum
from typing import Self, Any

from attrs import define, field, validators

from .enums import Confirmation, InsuranceProvider, OrderSourceCode
from ..common.enums import ValidateAddress
from ..common.models import (
    Value,
    Address,
    Weight,
    AddressValidation,
    Package,
)


@define
class TaxIdentifier:
    class TaxableEntityType(Enum):
        SHIPPER: str = "shipper"
        RECIPIENT: str = "recipient"
        IOR: str = "ior"

    class IdentifierType(Enum):
        VAT: str = "vat"
        EORI: str = "eori"
        SSN: str = "ssn"
        EIN: str = "ein"
        TIN: str = "tin"
        IOSS: str = "ioss"
        PAN: str = "pan"
        VOEC: str = "voec"
        PCCC: str = "pccc"
        OSS: str = "oss"
        PASSPORT: str = "passport"
        ABN: str = "abn"

    taxable_entity_type: TaxableEntityType = field(
        validator=validators.in_(TaxableEntityType)
    )
    identifier_type: IdentifierType = field(validator=validators.in_(IdentifierType))
    issuing_authority: str
    value: str


@define
class CustomsInformation:
    @define
    class InvoiceAdditionalDetail:
        freight_charge: Value
        insurance_charge: Value
        discount: Value
        other_charge: Value
        other_charge_description: str = field(default=None)

        @other_charge_description.validator
        def _validate_other_charge(self, attribute, value):
            if self.other_charge is not None and value is None:
                raise ValueError(
                    "other_charge_description required when other_charge is set"
                )

    class Contents(Enum):
        MERCHANDISE: str = "merchandise"
        DOCUMENTS: str = "documents"
        GIFT: str = "gift"
        RETURNED_GOODS: str = "returned_goods"
        SAMPLE: str = "sample"
        OTHER: str = "other"

    class NonDelivery(Enum):
        RETURN_TO_SENDER: str = "return_to_sender"
        TREAT_AS_ABANDONED: str = "treat_as_abandoned"

    class TermsOfTradeCode(Enum):
        EXW: str = "exw"
        FCA: str = "fca"
        CPT: str = "cpt"
        CIP: str = "cip"
        DPU: str = "dpu"
        DAP: str = "dap"
        DDP: str = "ddp"
        FAS: str = "fas"
        FOB: str = "fob"
        CFR: str = "fr"
        CIF: str = "cif"
        DDU: str = "ddu"
        DAF: str = "daf"
        DEQ: str = "deq"
        DES: str = "des"

    declaration: str
    invoice_additional_details: InvoiceAdditionalDetail
    importer_of_record: Address
    terms_of_trade_code: TermsOfTradeCode = field(
        validator=validators.in_(TermsOfTradeCode)
    )
    contents: Contents = field(
        default=Contents.MERCHANDISE, validator=validators.in_(Contents)
    )
    contents_explanation: str = field(default=None)
    non_delivery: NonDelivery = field(
        default=NonDelivery.RETURN_TO_SENDER, validator=validators.in_(NonDelivery)
    )

    @contents_explanation.validator
    def _validate_contents_explanation(self, attribute, value):
        if self.contents == self.Contents.OTHER and value is None:
            raise ValueError(
                "'contents_explanation' is required when 'contents' are 'other'"
            )


@define
class AdvancedOptions:
    @define
    class FedexFreight:
        shipper_load_and_count: str
        booking_confirmation: str

    @define
    class CollectOnDelivery:
        class PaymentType(Enum):
            ANY: str = "any"
            CASH: str = "cash"
            CASH_EQUIVALENT: str = "cash_equivalent"
            NONE: str = "none"

        payment_type: PaymentType = field(validator=validators.in_(PaymentType))
        payment_amount: Value

    @define
    class DangerousGoodsContact:
        name: str
        phone: str

    class BillToParty(Enum):
        RECIPIENT: str = "recipient"
        THIRD_PARTY: str = "third_party"

    class OriginType(Enum):
        PICKUP: str = "pickup"
        DROP_OFF: str = "drop_off"

    contains_alcohol: bool = field(default=False)
    delivered_duty_paid: bool = field(default=False)
    dry_ice: bool = field(default=False)
    dry_ice_weight: Weight = field(default=None)
    non_machinable: bool = field(default=False)
    saturday_delivery: bool = field(default=False)
    bill_to_account: str = field(default=None)
    bill_to_country_code: str = field(default=None)
    bill_to_party: BillToParty = field(default=None)
    bill_to_postal_code: str = field(default=None)
    fedex_freight: FedexFreight = field(default=None)
    use_ups_ground_freight_pricing: bool = field(default=None)
    freight_class: str = field(default=None)
    custom_field1: str = field(default=None)
    custom_field2: str = field(default=None)
    custom_field3: str = field(default=None)
    origin_type: OriginType = field(default=None)
    additional_handling: bool = field(default=None)
    shipper_release: bool = field(default=None)
    collect_on_delivery: CollectOnDelivery = field(default=None)
    third_party_consignee: bool = field(default=False)
    dangerous_goods: bool = field(default=False)
    dangerous_goods_contact: DangerousGoodsContact = field(default=None)

    ancillary_endorsements_option: str = field(default=None)
    return_pickup_attempts: int = field(default=None)
    own_document_upload: bool = field(default=False)
    limited_quantity: bool = field(default=False)
    event_notification: bool = field(default=False)

    @use_ups_ground_freight_pricing.validator
    def _use_ups_ground_freight_pricing(self, attribute, value):
        if value is not None and self.freight_class is None:
            raise ValueError(
                "freight_class cannot be None when "
                "use_ups_ground_freight_pricing is set"
            )


@define
class ShipmentRequest:
    carrier_id: str
    service_code: str
    ship_to: Address
    ship_date: str = field(default=None)
    validate_address: ValidateAddress = field(
        default=ValidateAddress.NO_VALIDATION, validator=validators.in_(ValidateAddress)
    )
    advanced_options: AdvancedOptions = field(default=None)
    confirmation: Confirmation = field(
        default=Confirmation.NONE, validator=validators.in_(Confirmation)
    )
    tags: list[str] = field(default=[])
    is_return: bool = field(default=False)
    customs: list[CustomsInformation] = field(default=None)
    warehouse_id: str = field(default=None)
    ship_from: Address = field(default=None)
    return_to: Address = field(default=None)
    items: list[str] = field(default=[])
    external_order_id: str = field(default=None)
    tax_identifiers: list[TaxIdentifier] = field(default=None)
    external_shipment_id: str = field(default=None)
    shipment_number: str = field(default=None)
    insurance_provider: InsuranceProvider = field(
        default=InsuranceProvider.NONE, validator=validators.in_(InsuranceProvider)
    )
    order_source_code: OrderSourceCode = field(default=None)
    packages: list[Package] = field(default=None)
    comparison_rate_type: str = field(default=None)


@define(kw_only=True)
class Shipment(ShipmentRequest):
    """Subclassed from ShipmentRequest to avoid repeating many fields."""

    class Status(Enum):
        PENDING: str = "pending"
        PROCESSING: str = "processing"
        LABEL_PURCHASED: str = "label_purchased"
        CANCELLED: str = "cancelled"

    shipment_id: str
    created_at: str
    modified_at: str
    shipping_rule_id: str
    errors: list[str] = field(default=[])
    shipment_status: Status = field(
        default=Status.PENDING, validator=validators.in_(Status)
    )
    total_weight: Weight = field(default=None)
    address_validation: AddressValidation = field(default=None)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        ship_to = Address(**data.pop("ship_to"))
        ship_from = Address(**data.pop("ship_from"))
        return_to = Address(**data.pop("return_to"))
        packages = [Package.from_dict(p) for p in data.pop("packages")]
        total_weight = Weight(**data.pop("total_weight"))
        advanced_options = AdvancedOptions(**data.pop("advanced_options"))

        return cls(
            ship_to=ship_to,
            ship_from=ship_from,
            advanced_options=advanced_options,
            return_to=return_to,
            packages=packages,
            total_weight=total_weight,
            **data,
        )
