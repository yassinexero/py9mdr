from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
from pydantic_core import PydanticCustomError
from typing import List
from datetime import datetime


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        # Rule 1: Mission ID must start with "M"
        if not self.mission_id.startswith("M"):
            raise PydanticCustomError(
                "mission_id_error",
                "Mission ID must start with 'M'"
            )

        # Rule 2: Must have at least one Captain or Commander
        if not any(
            member.rank in [Rank.captain, Rank.commander]
            for member in self.crew
        ):
            raise PydanticCustomError(
                "rank_error",
                "Mission must have at least one Captain or Commander"
            )

        # Rule 3: Long missions need 50% experienced crew (>=5 years)
        if self.duration_days > 365:
            experienced = [
                member for member in self.crew if member.years_experience >= 5
            ]
            if len(experienced) < len(self.crew) / 2:
                raise PydanticCustomError(
                    "experience_error",
                    "Long missions require ≥50% experienced crew"
                )

        # Rule 4: All crew must be active
        if not all(member.is_active for member in self.crew):
            raise PydanticCustomError(
                "active_error",
                "All crew members must be active"
            )

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)

    # VALID MISSION
    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2025, 1, 1, 10, 0, 0),
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="CM1",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=45,
                    specialization="Mission Command",
                    years_experience=20,
                ),
                CrewMember(
                    member_id="CM2",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=10,
                ),
                CrewMember(
                    member_id="CM3",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=6,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")

        print("Crew members:")
        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )

    except Exception as e:
        print(e)

    print("=" * 40)

    # INVALID MISSION
    try:
        SpaceMission(
            mission_id="M_BAD",
            mission_name="Test Mission",
            destination="Moon",
            launch_date=datetime(2025, 1, 1, 10, 0, 0),
            duration_days=100,
            budget_millions=100.0,
            crew=[
                CrewMember(
                    member_id="CM1",
                    name="Bob",
                    rank=Rank.officer,
                    age=30,
                    specialization="Tech",
                    years_experience=2,
                )
            ],
        )

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
