# Release Notes - KVM1 Astrology Engine v2.0.0

**Release Date**: 2026-08-06  
**Tag**: `v2.0.0`

---

## Executive Overview

KVM1 Astrology Engine Release v2.0.0 represents a complete architectural transformation into an enterprise-grade, high-performance Universal Astrology Engine built on Clean Architecture and SOLID principles.

---

## What's New in v2.0.0

1. **Framework-Independent Domain Layer**: Pure `@dataclass(frozen=True)` entities.
2. **Single Source of Truth Astronomy**: Swiss Ephemeris (`pyswisseph`) C-bindings are wrapped exclusively in `SwissephService`.
3. **Pluggable Registries**:
   - `EngineRegistry`: Supports pluggable calculation systems (Vedic, KP, Jaimini, Nadi, Muhurtha, Prasna).
   - `VargaRegistry`: Supports 14 Parashari divisional charts (D2 to D60).
   - `RuleRegistry`: Manages priority-evaluated astrological rules across 7 categories.
4. **Resilient Infrastructure Adapters**:
   - `CompositeGeocoder` fallback chain: `Offline Database` -> `GeoNames` -> `Nominatim` -> `Google Maps`.
   - `TwoLevelCache`: Combined L1 Memory + L2 Redis caching.
5. **Prediction & Report Engine**: Multilingual interpretation engine (Tamil & English).

---

## Verification & Compatibility

- **Golden Chart Regression**: 39/39 Golden snapshot chart tests passed with 0 divergence.
- **Unit & Integration Coverage**: 55/55 Unit & Integration tests passed.
- **Total Test Suite**: 94/94 Tests Passing.
