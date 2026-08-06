# KVM1 Astrology Engine - Master Architecture Specification (v2.0.0)

## Executive Summary

KVM1 is a Universal Astrology Calculation Engine designed following **Clean Architecture**, **SOLID Principles**, and **Domain-Driven Design (DDD)**.

---

## Core Architectural Guiding Rules

1. **Framework Independence**: The Domain Layer (`domain/models/`) is 100% pure Python (`frozen=True` dataclasses). Zero dependencies on FastAPI, Pydantic, or SQLAlchemy.
2. **Single Source of Truth**: Swiss Ephemeris (`SwissephService`) is the single astronomical source of truth. All downstream engines (`VedicEngine`, `VargaRegistry`, `RuleEngine`, `PredictionEngine`) read exclusively from `CalculationContext.astronomical_state`.
3. **Immutability & Traceability**: `CalculationContext` flows through the pipeline stages sequentially, returning enriched context envelopes with explicit stage execution metrics and trace IDs.
4. **Pluggable Registries**:
   - `EngineRegistry`: Pluggable astrology engines (Vedic, KP, Jaimini, Nadi, Muhurtha, Prasna).
   - `VargaRegistry`: 14 Parashari divisional chart calculators.
   - `RuleRegistry`: Priority-ordered astrological rules.

---

## Layered System Topology

```
+-----------------------------------------------------------------------+
|                           Presentation Layer                          |
|         - FastAPI Routers          - JSONResponseBuilder              |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                      Calculation Pipeline Stage                       |
|   LocationService -> TimezoneService -> JulianDay -> SwissephService  |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                     Domain Engine & Rule System                       |
|   - VedicEngine                    - VargaRegistry (14 Vargas)        |
|   - RuleEngine (7 Categories)      - PredictionEngine                 |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                         Infrastructure Adapters                       |
|   - CompositeGeocoder              - TwoLevelCache (L1/L2)            |
|   - Dependency Injection Container (Pure Python DIP)                  |
+-----------------------------------------------------------------------+
```
