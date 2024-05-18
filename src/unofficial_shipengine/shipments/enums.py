from enum import Enum


class Confirmation(Enum):
    NONE: str = "none"
    DELIVERY: str = "delivery"
    SIGNATURE: str = "signature"
    ADULT_SIGNATURE: str = "adult_signature"
    DIRECT_SIGNATURE: str = "direct_signature"
    DELIVERY_MAILED: str = "delivery_mailed"
    VERBAL_CONFIRMATION: str = "verbal_confirmation"


class InsuranceProvider(Enum):
    NONE: str = "none"
    SHIPSURANCE: str = "shipsurance"
    CARRIER: str = "carrier"
    THIRD_PARTY: str = "third_party"


class OrderSourceCode(Enum):
    AMAZON_CA: str = "amazon_ca"
    AMAZON_US: str = "amazon_us"
    BRIGHTPEARL: str = "brightpearl"
    CHANNEL_ADVISOR: str = "channel_advisor"
    CRATEJOY: str = "cratejoy"
    EBAY: str = "ebay"
    ETSY: str = "etsy"
    JANE: str = "jane"
    GROUPON_GOODS: str = "groupon_goods"
    MAGENTO: str = "magento"
    PAYPAL: str = "paypal"
    SELLER_ACTIVE: str = "seller_active"
    SHOPIFY: str = "shopify"
    STITCH_LABS: str = "stitch_labs"
    SQUARESPACE: str = "squarespace"
    THREE_DCART: str = "three_dcart"
    TOPHATTER: str = "tophatter"
    WALMART: str = "walmart"
    WOO_COMMERCE: str = "woo_commerce"
    VOLUSION: str = "volusion"
