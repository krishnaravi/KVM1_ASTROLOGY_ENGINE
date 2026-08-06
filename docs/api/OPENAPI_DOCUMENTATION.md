# KVM1 Astrology Engine - OpenAPI 3.0 Documentation

## Overview

The **KVM1 Astrology Engine** exposes a RESTful HTTP API built with FastAPI. The OpenAPI 3.0 specification details all endpoints, request parameter schemas, and response formats.

---

## Base URL

`http://localhost:8000`

---

## Endpoints Summary

| Method | Endpoint | Description | Public Schema |
|---|---|---|---|
| `GET` | `/health` | Health check endpoint | Yes |
| `GET` | `/api/version` | Engine metadata and versioning details | Yes (Internal) |
| `GET` | `/api/metrics` | System cache statistics & performance metrics | Yes (Internal) |
| `GET` | `/api/rasi-chart` | Rasi chart calculation | Yes |
| `GET` | `/api/planet-positions` | Planetary longitudes and signs | Yes |
| `GET` | `/api/houses` | House cusps and occupant mappings | Yes |
| `GET` | `/api/lagna` | Ascendant calculations | Yes |
| `GET` | `/calculate-horoscope` | Legacy horoscope calculation endpoint | Yes |

---

## Endpoint Details

### `GET /health`
Returns system health status.

**Response (200 OK)**:
```json
{
  "status": "healthy"
}
```

### `GET /api/version`
Returns EngineMetadata version numbers and ephemeris details.

**Response (200 OK)**:
```json
{
  "status": "success",
  "metadata": {
    "api_version": "1.0.0",
    "engine_version": "2.0.0",
    "rule_version": "2.0.0",
    "ephemeris_version": "SwissEph 2.10",
    "build_version": "v2.0.0-production",
    "ayanamsa": "Lahiri"
  }
}
```

### `GET /api/metrics`
Returns runtime cache statistics and system metrics.

**Response (200 OK)**:
```json
{
  "status": "success",
  "engine": "2.0.0",
  "cache_stats": {
    "l1_memory": {
      "entries_count": 12,
      "hits": 45,
      "misses": 3,
      "hit_ratio": 0.9375
    },
    "l2_redis_connected": false
  }
}
```
