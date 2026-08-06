from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from domain.models.birth_data import BirthData


@dataclass
class ValidationResult:
    """
    Result object returned by BirthDataValidator.
    """
    is_valid: bool
    errors: List[str] = field(default_factory=list)


class BirthDataValidator:
    """
    Boundary validator for BirthData inputs prior to calculation pipeline execution.
    Framework-independent pure Python validation layer.
    """

    @staticmethod
    def validate(birth_data: BirthData) -> ValidationResult:
        errors: List[str] = []

        # 1. Validate Date (YYYY-MM-DD)
        if not birth_data.date:
            errors.append("Date of birth is required.")
        else:
            try:
                datetime.strptime(birth_data.date, "%Y-%m-%d")
            except ValueError:
                errors.append(f"Invalid date format '{birth_data.date}'. Expected YYYY-MM-DD.")

        # 2. Validate Time (HH:MM or HH:MM:SS)
        if not birth_data.time:
            errors.append("Time of birth is required.")
        else:
            time_valid = False
            for fmt in ("%H:%M", "%H:%M:%S"):
                try:
                    datetime.strptime(birth_data.time, fmt)
                    time_valid = True
                    break
                except ValueError:
                    pass
            if not time_valid:
                errors.append(f"Invalid time format '{birth_data.time}'. Expected HH:MM or HH:MM:SS.")

        # 3. Validate Location Input
        has_place = bool(birth_data.birth_place and birth_data.birth_place.strip())
        has_coords = birth_data.latitude is not None and birth_data.longitude is not None

        if not has_place and not has_coords:
            errors.append("Either 'birth_place' or both 'latitude' and 'longitude' must be provided.")

        if birth_data.latitude is not None:
            if not (-90.0 <= birth_data.latitude <= 90.0):
                errors.append(f"Latitude '{birth_data.latitude}' out of range [-90.0, 90.0].")

        if birth_data.longitude is not None:
            if not (-180.0 <= birth_data.longitude <= 180.0):
                errors.append(f"Longitude '{birth_data.longitude}' out of range [-180.0, 180.0].")

        return ValidationResult(is_valid=len(errors) == 0, errors=errors)
