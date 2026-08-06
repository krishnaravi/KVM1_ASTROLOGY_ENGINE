# Domain Model Documentation

## Domain Model Taxonomy

All domain models reside in `domain/` and are defined as immutable Python dataclasses (`@dataclass(frozen=True)`).

| Class Name | File Path | Role / Description |
|---|---|---|
| `EngineMetadata` | `domain/versioning.py` | Immutable container for system, engine, rule, and ephemeris versions. |
| `BirthData` | `domain/models/birth_data.py` | Input entity representing raw birth date, time, and location details. |
| `ResolvedLocation` | `domain/models/location.py` | Entity representing resolved geographic coordinates and provider metadata. |
| `TimezoneContext` | `domain/models/timezone.py` | Entity capturing IANA timezone string, UTC offset, and DST status. |
| `JulianDayContext` | `domain/models/time_context.py` | Entity representing local/UTC datetime strings and Universal Time Julian Day. |
| `EphemerisContext` | `domain/models/ephemeris_context.py` | Entity recording active ephemeris version, ayanamsa name, and degree. |
| `AstronomicalState` | `domain/models/astronomical_state.py` | Immutable Single Source of Truth astronomical output from Swiss Ephemeris. |
| `CalculationContext` | `domain/models/calculation_context.py` | Pipeline data envelope unifying all contextual calculation entities. |
| `CalculationAuditLog` | `domain/models/audit_log.py` | Audit entity capturing execution lineage and metadata. |
| `Planet` | `domain/planet.py` | Pure astronomical planet position entity. |
| `ChartPlanet` | `domain/chart.py` | Horoscope-placed planet entity carrying house placement and strength scores. |
| `House` | `domain/house.py` | House cusp degree and sign entity. |
