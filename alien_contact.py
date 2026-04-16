from enum import Enum
from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError
from datetime import datetime
from typing import Optional


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Field(...)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType = Field(...)
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_rules(self) -> "AlienContact":
        # Rule 1: ID must start with "AC"
        if not self.contact_id.startswith("AC"):
            raise PydanticCustomError(
                "contact_id_error",
                "Contact ID must start with 'AC'"
            )

        # Rule 2: Physical contact must be verified
        if self.contact_type == ContactType.physical and not self.is_verified:
            raise PydanticCustomError(
                "verification_error",
                "Physical contact must be verified"
            )
        # Rule 3: Telepathic requires at least 3 witnesses
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise PydanticCustomError(
                "witness_error",
                "Telepathic contact requires at least 3 witnesses"
            )

        # Rule 4: Strong signal must include message
        if self.signal_strength > 7.0 and not self.message_received:
            raise PydanticCustomError(
                "message_error",
                "Strong signals must include a message"
            )

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)

    # VALID CASE
    try:
        contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2024, 5, 4),
            location="Area 51",
            contact_type=ContactType.radio,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )

        print("Valid contact report:")
        print(f"ID: {contact.contact_id}")
        print(f"Type: {contact.contact_type.value}")
        print(f"Location: {contact.location}")
        print(f"Signal: {contact.signal_strength}/10")
        print(f"Duration: {contact.duration_minutes} minutes")
        print(f"Witnesses: {contact.witness_count}")
        print(f"Message: {contact.message_received}")
        print(f"x{contact.timestamp}")

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])

    print("=" * 40)

    # INVALID CASE (telepathic rule)
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-01-01T10:00:00",
            location="Mars Base",
            contact_type=ContactType.telepathic,
            signal_strength=5.0,
            duration_minutes=30,
            witness_count=2,
        )

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
