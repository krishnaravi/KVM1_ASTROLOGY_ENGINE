# KVM1 Astrology Engine - Universal Astrology Calculation & Prediction Engine (v2.1.0)

[![Build & Test Status](https://img.shields.io/badge/tests-126%20passed-brightgreen.svg)]()
[![Architecture](https://img.shields.io/badge/architecture-Clean%20Architecture%20%2B%20SOLID-blue.svg)]()
[![Version](https://img.shields.io/badge/release-v2.1.0-gold.svg)]()

**KVM1 Astrology Engine** is an enterprise-grade, high-performance Universal Astrology Calculation and Prediction Engine built using **Clean Architecture**, **SOLID Principles**, and **Domain-Driven Design**.

---

## Key Highlights

- **Framework-Independent Domain Layer**: Pure Python `@dataclass(frozen=True)` entities.
- **Single Source of Truth**: Swiss Ephemeris (`pyswisseph` C-bindings) is the sole astronomical source of truth.
- **Resilient Infrastructure**: Composite Geocoder fallback chain (`Offline DB` -> `GeoNames` -> `Nominatim` -> `Google`) and Two-Level Cache (`L1` Memory + `L2` Redis).
- **Pluggable Registries**:
  - `EngineRegistry`: Pluggable astrology engines (Vedic, KP, Jaimini, Nadi, Muhurtha, Prasna).
  - `VargaRegistry`: 14 Parashari divisional chart calculators (D2, D3, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60).
  - `RuleRegistry`: Priority-ordered rule engine with 7 categories.
- **Prediction Engine**: Multilingual interpretation engine (Tamil first, English ready).
- **100% Backward Compatible**: Preserves full backward compatibility across all legacy API contracts.

---

## Quickstart

```bash
# Clone repository
git clone https://github.com/krishnaravi/KVM1_ASTROLOGY_ENGINE.git
cd KVM1_ASTROLOGY_ENGINE

# Create an isolated test environment and run the verified suite
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -ra

# Start local server
uvicorn main:app --reload --port 8000
```

---

## Architecture Documentation

See [docs/architecture/ARCHITECTURE_MASTER.md](file:///c:/Users/DELL/Documents/GitHub/KVM1_ASTROLOGY_ENGINE/docs/architecture/ARCHITECTURE_MASTER.md) and [docs/DEVELOPER_GUIDE.md](file:///c:/Users/DELL/Documents/GitHub/KVM1_ASTROLOGY_ENGINE/docs/DEVELOPER_GUIDE.md).

## v2.1.0 verification

- Source commit: `5e8bc7fef2cead2af4e7a4d90df223e593ad53a5`
- Regression verification: 126 collected, 126 passed, 0 failed, 0 skipped, 0 warnings.
- Test date: 2026-09-08 (isolated Python 3.12 environment).
- The historical 94-test figure applies to v2.0.0 only; it is not the current v2.1.0 result.
