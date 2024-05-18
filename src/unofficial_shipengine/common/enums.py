from enum import Enum


class ValidateAddress(Enum):
    NO_VALIDATION: str = "no_validation"
    VALIDATE_ONLY: str = "validate_only"
    VALIDATE_AND_CLEAN: str = "validate_and_clean"
