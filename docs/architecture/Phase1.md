# Phase 1 Architecture: Framework-Independent Domain & Validation Layer

## Architecture Overview

Phase 1 establishes the clean domain foundation for KVM1 Astrology Engine.

```
       +-------------------------------------------------------+
       |                  Presentation Layer                   |
       |                (routers/, main.py)                    |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |                   Validation Layer                    |
       |          (validators/birth_data_validator.py)         |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |               Pure Domain Core (No Libs)              |
       |  - CalculationContext     - AstronomicalState         |
       |  - BirthData              - ResolvedLocation          |
       |  - TimezoneContext        - JulianDayContext          |
       |  - EphemerisContext       - CalculationAuditLog       |
       |  - EngineMetadata         - Planet / House            |
       +-------------------------------------------------------+
```

## Key Components

1. **`EngineMetadata`** (`domain/versioning.py`):
   - Immutable system-wide versioning container (`api_version`, `engine_version`, `rule_version`, `ephemeris_version`, `build_version`, `ayanamsa`).

2. **`CalculationContext`** (`domain/models/calculation_context.py`):
   - Immutable envelope object carrying `trace_id`, input parameters, resolved geographic location, timezone details, Julian day computations, ephemeris settings, and single-source-of-truth `AstronomicalState`.

3. **`BirthDataValidator`** (`validators/birth_data_validator.py`):
   - Pure boundary validator verifying input dates (`YYYY-MM-DD`), times (`HH:MM`), location strings, and geographic coordinate ranges (`[-90, 90]`, `[-180, 180]`).
