# Phase 2 Architecture: Core Interfaces & Dependency Injection Container

## Overview

Phase 2 establishes the core abstraction layer and lightweight dependency injection infrastructure for KVM1 Astrology Engine.

```
       +-------------------------------------------------------+
       |               Application Container                   |
       |             (infrastructure/container.py)             |
       +---------------------------+---------------------------+
                                   | Registers & Resolves
                                   v
       +-------------------------------------------------------+
       |              Abstract Interface Contracts              |
       |                  (core/interfaces/)                   |
       |  - IGeocoderProvider      - ICacheProvider            |
       |  - ITimezoneService       - IJulianDayService         |
       |  - ISwissephService       - IAstrologyEngine          |
       |  - IRule / IRuleEngine    - IAuditLogger              |
       +-------------------------------------------------------+
```

## Interface Taxonomy

- `IGeocoderProvider`: Geocoding adapter abstraction (`geocode(place_name) -> ResolvedLocation`).
- `ICacheProvider`: Key-value cache abstraction (`get`, `set`, `delete`).
- `ITimezoneService`: Spatial lat/lon to IANA timezone & DST offset resolution.
- `IJulianDayService`: Local to UTC datetime & Julian Day computation.
- `ISwissephService`: Swiss Ephemeris Single Source of Truth calculation contract.
- `IAstrologyEngine`: System engine contract (`calculate(context) -> Dict`).
- `IRule` & `IRuleEngine`: Rule evaluation taxonomy and dispatcher.
- `IAuditLogger`: Structured calculation audit logging contract.
