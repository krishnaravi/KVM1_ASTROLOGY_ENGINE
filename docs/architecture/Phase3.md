# Phase 3 Architecture: Core Services & CalculationContext Pipeline

## 1. Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    actor Client
    participant Router as API Controller (routers/chart.py)
    participant Validator as BirthDataValidator
    participant Pipe as CalculationPipeline
    participant LocService as LocationService
    participant TZService as TimezoneService
    participant JDService as JulianDayService
    participant SweService as SwissephService
    participant AuditLogger as AuditLoggingService

    Client->>Router: Request (date, time, birth_place / lat, lon)
    Router->>Validator: validate(BirthData)
    Validator-->>Router: ValidationResult (OK)

    Router->>Pipe: execute(birth_data, trace_id)
    Note over Pipe: Stage 0: Create Initial CalculationContext(v0)

    Pipe->>LocService: process(context_v0)
    LocService-->>Pipe: context_v1 [ResolvedLocation Enriched]

    Pipe->>TZService: process(context_v1)
    TZService-->>Pipe: context_v2 [TimezoneContext Enriched]

    Pipe->>JDService: process(context_v2)
    JDService-->>Pipe: context_v3 [JulianDayContext Enriched]

    Pipe->>SweService: process(context_v3)
    SweService-->>Pipe: context_v4 [AstronomicalState Enriched (Single Source of Truth)]

    Pipe->>AuditLogger: create_audit_log_from_context(context_v4)
    AuditLogger-->>Pipe: CalculationAuditLog
    Pipe-->>Router: Final CalculationContext (v4)
    Router-->>Client: Response (Trace ID + Chart Data)
```

## 2. Pipeline State Diagram

```mermaid
stateDiagram-v2
    [*] --> ContextInit: birth_data + trace_id (v0)
    ContextInit --> LocationResolved: LocationService (v1)
    LocationResolved --> TimezoneResolved: TimezoneService (v2)
    TimezoneResolved --> JulianDayComputed: JulianDayService (v3)
    JulianDayComputed --> AstronomicalStateFinalized: SwissephService (v4)
    AstronomicalStateFinalized --> AuditLogged: AuditLoggingService
    AuditLogged --> [*]
```

## 3. Error Flow Diagram

```mermaid
graph TD
    REQ[Request Input] --> VAL{BirthDataValidator}
    VAL -- Invalid --> ERR_VAL[ValidationError]
    VAL -- Valid --> LOC{LocationService}
    LOC -- Failed --> ERR_LOC[LocationResolutionError]
    LOC -- Success --> TZ{TimezoneService}
    TZ -- Failed --> ERR_TZ[TimezoneResolutionError]
    TZ -- Success --> JD{JulianDayService}
    JD -- Failed --> ERR_JD[JulianDayCalculationError]
    JD -- Success --> SWE{SwissephService}
    SWE -- Failed --> ERR_SWE[SwissEphemerisError]
    SWE -- Success --> OK[Finalized CalculationContext]

    ERR_VAL --> AUDIT[Audit Logging & Standard HTTP 400/422/500 Response]
    ERR_LOC --> AUDIT
    ERR_TZ --> AUDIT
    ERR_JD --> AUDIT
    ERR_SWE --> AUDIT
```

## 4. Unified Error Hierarchy Taxonomy

All system exceptions inherit from `EngineError` (`core/errors.py`) and expose:
- `trace_id`: Unique request UUID.
- `stage_id`: Pipeline stage identifier string.
- `error_code`: Machine-readable error code.
- `human_message`: Human-readable error description.

| Exception Class | Base Class | Error Code | Pipeline Stage |
|---|---|---|---|
| `ValidationError` | `EngineError` | `VALIDATION_ERROR` | `VALIDATION` |
| `LocationResolutionError` | `EngineError` | `LOCATION_RESOLUTION_ERROR` | `STAGE_LOCATION` |
| `TimezoneResolutionError` | `EngineError` | `TIMEZONE_RESOLUTION_ERROR` | `STAGE_TIMEZONE` |
| `JulianDayCalculationError` | `EngineError` | `JULIAN_DAY_CALCULATION_ERROR` | `STAGE_JULIAN_DAY` |
| `SwissEphemerisError` | `EngineError` | `SWISS_EPHEMERIS_ERROR` | `STAGE_SWISS_EPHEMERIS` |
| `PipelineExecutionError` | `EngineError` | `PIPELINE_EXECUTION_ERROR` | `PIPELINE_ORCHESTRATION` |
