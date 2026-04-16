from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(...)
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)

    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 1, 10, 0, 0),
            is_operational=True,
            notes="Regular maintenance required every 6 months."
        )

        print("Valid station created:")
        print(f"ID: {station.station_id}")
        print(f"Name: {station.name}")
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(
            f"Status: "
            f"{'Operational' if station.is_operational else 'Non-operational'}"
        )

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])

    print("=" * 40)

    try:
        SpaceStation(
            station_id="ISS004",
            name="Station X",
            crew_size=50,
            power_level=50.0,
            oxygen_level=10.0,
            last_maintenance=datetime(2024, 1, 1, 10, 0, 0),
            is_operational=True,
            notes="This station has invalid data."
        )

    except ValidationError as e:
        print("Expected validation error:")
        for err in e.errors():
            print(err["msg"])


if __name__ == "__main__":
    main()
