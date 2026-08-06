# KVM1 Astrology Engine - API Reference Guide

## API Endpoints Overview

### 1. `GET /api/rasi-chart`
Calculates Rasi chart and full planetary analysis.

**Query Parameters**:
- `date` (string, required): Format `YYYY-MM-DD` (e.g. `1990-05-15`).
- `time` (string, required): Format `HH:MM` (e.g. `10:30`).
- `latitude` (float, required): Latitude in degrees (-90.0 to 90.0).
- `longitude` (float, required): Longitude in degrees (-180.0 to 180.0).

---

### 2. `GET /api/planet-positions`
Calculates raw planetary longitudes, speeds, and sign placements.

**Query Parameters**: Same as `/api/rasi-chart`.

---

### 3. `GET /api/houses`
Calculates house cusps and occupant mappings.

**Query Parameters**: Same as `/api/rasi-chart`.

---

### 4. `GET /api/lagna`
Calculates Ascendant (Lagna) sign, degree, nakshatra, and pada.

**Query Parameters**: Same as `/api/rasi-chart`.

---

### 5. `GET /health`
Returns system health status.

---

### 6. `GET /api/version`
Returns Engine Metadata (`api_version`, `engine_version`, `ephemeris_version`, `ayanamsa`).

---

### 7. `GET /api/metrics`
Returns runtime cache statistics and system performance metrics.
