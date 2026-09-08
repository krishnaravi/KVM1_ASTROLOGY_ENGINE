# CHANGELOG - KVM1 Astrology Engine

All notable changes to the KVM1 Astrology Engine are documented in this file.
## [2.1.0] - 2026-09-04

### Release hygiene
- Aligned engine and build metadata with the v2.1.0 release.
- Added the deployment Dockerfile to source control without changing its behavior.
- Added a development/test dependency manifest and v2.1.0 release notes.

### Verified
- Regression suite: 126 collected, 126 passed, 0 failed, 0 skipped, 0 warnings.
- Verified from source commit `5e8bc7fef2cead2af4e7a4d90df223e593ad53a5`.


## [2.0.0] - 2026-08-06

### Added
- **Phase 1 & 1.1**: Framework-Independent Domain Layer (`BirthData`, `ResolvedLocation`, `TimezoneContext`, `JulianDayContext`, `EphemerisContext`, `AstronomicalState`, `CalculationContext`). Added immutable `EngineMetadata` and `BirthDataValidator`.
- **Phase 2**: Core Interface Contracts (`IGeocoderProvider`, `ICacheProvider`, `ITimezoneService`, `IJulianDayService`, `ISwissephService`, `IAstrologyEngine`, `IRule`, `IRuleEngine`, `IAuditLogger`, `IPipelineStage`) and pure Python Dependency Injection Container.
- **Phase 3**: Calculation Pipeline Stage (`CalculationPipeline`, `LocationService`, `TimezoneService`, `JulianDayService`, `SwissephService`, `AuditLoggingService`).
- **Phase 4**: Infrastructure Adapters (`CompositeGeocoder` fallback chain, `MemoryCache` L1, `RedisCache` L2, `TwoLevelCache`, `/api/version`, `/api/metrics`).
- **Phase 5**: Vedic Core Calculation Engine (`EngineRegistry`, `VedicPlanetEngine`, `VedicHouseEngine`, `VedicHouseLordEngine`, `VedicDrishtiEngine`, `VedicStrengthEngine`, `VedicEngine`).
- **Phase 6**: 14 Parashari Divisional Chart Calculators & `VargaRegistry` (D2, D3, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60).
- **Phase 7**: Rule Engine Framework & Rule Taxonomy Categories (`RuleRegistry`, `RuleEngine`, priority evaluation, 7 categories).
- **Phase 8**: Prediction Engine, Multilingual `ExplanationEngine`, `ReportBuilder`, and `JSONResponseBuilder`.
- **Phase 9**: Production Stabilization, Documentation Suite, OpenAPI Spec, and Release v2.0.0.

### Verified
- 100% Backward Compatibility with legacy API contracts.
- 94/94 Tests Passing cleanly.
