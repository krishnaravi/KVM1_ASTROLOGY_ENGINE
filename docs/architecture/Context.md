# CalculationContext Architecture & Lifecycle

## Overview

The `CalculationContext` is the immutable data envelope that travels through every stage of the KVM1 Astrology Engine pipeline.

## Structure

- **`trace_id`**: Unique UUID string assigned per calculation request.
- **`birth_data`**: Client birth details (`date`, `time`, `birth_place`, `latitude`, `longitude`).
- **`resolved_location`**: Geocoded geographic coordinates (`resolved_name`, `latitude`, `longitude`, `provider`).
- **`timezone_context`**: Resolved IANA timezone and DST details (`iana_timezone`, `utc_offset`, `utc_offset_seconds`, `is_dst`).
- **`julian_day_context`**: Converted local/UTC date-time strings and computed astronomical Julian Day (`local_datetime`, `utc_datetime`, `julian_day`).
- **`ephemeris_context`**: Swiss Ephemeris metadata (`ephemeris_version`, `ayanamsa_name`, `ayanamsa_value`).
- **`astronomical_state`**: Single Source of Truth astronomical positions (`planets`, `houses`, `ayanamsa_deg`).
- **`engine_metadata`**: Diagnostic and rule evaluation output container.

## Context Lifecycle

1. **Instantiation**: Boundary controllers initialize `CalculationContext` with request `trace_id` and raw `BirthData`.
2. **Enrichment**: Location, Timezone, and Julian Day services populate resolution contexts.
3. **Ephemeris Execution**: `SwissephService` computes `AstronomicalState` **once** and attaches it to the context.
4. **Engine & Rule Execution**: Downstream engines read from `context.astronomical_state` to perform analysis without recomputing positions.
5. **Auditing**: `CalculationAuditLog` captures the finalized `CalculationContext` for audit storage.
