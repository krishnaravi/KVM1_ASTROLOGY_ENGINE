# Phase 4 Architecture: Infrastructure Adapters & System Monitoring

## Overview

Phase 4 completes the infrastructure adapters layer for KVM1 Astrology Engine.

```
       +-------------------------------------------------------+
       |                  Presentation Layer                   |
       |  - GET /health           - GET /api/version           |
       |  - GET /api/metrics      - GET /api/rasi-chart        |
       +---------------------------+---------------------------+
                                   |
                                   v
       +-------------------------------------------------------+
       |               Infrastructure Adapters                 |
       |                                                       |
       |  [Geocoding Priority Chain]                           |
       |  Offline DB -> GeoNames -> Nominatim -> Google Maps   |
       |                                                       |
       |  [Two-Level Cache]                                    |
       |  L1 Memory Cache <----------> L2 Redis Cache          |
       +-------------------------------------------------------+
```

## System Endpoints

- **`GET /health`**: Health status endpoint (`{"status": "healthy"}`).
- **`GET /api/version`**: Versioning details (`api_version`, `engine_version`, `rule_version`, `ephemeris_version`, `build_version`, `ayanamsa`).
- **`GET /api/metrics`**: System performance metrics and L1/L2 cache statistics.
