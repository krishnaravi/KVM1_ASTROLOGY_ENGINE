# Phase 5 Architecture: Vedic Core Calculation Engine & Engine Registry

## Overview

Phase 5 implements the Vedic Core Calculation Engine and pluggable Engine Registry.

```
                      +-----------------------------+
                      |     CalculationContext      |
                      |  (Single Source of Truth)   |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |       EngineRegistry        |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |         VedicEngine         |
                      +--------------+--------------+
                                     |
         +-------------------+-------+-------+-------------------+
         |                   |               |                   |
         v                   v               v                   v
+------------------+ +---------------+ +---------------+ +---------------+
|   Planet Engine  | |  House Engine | |   Lord Engine | | Drishti Engine|
+------------------+ +---------------+ +---------------+ +---------------+
                                     |
                                     v
                             +---------------+
                             |Strength Engine|
                             +---------------+
```

## Sub-Engine Responsibilities

- **`VedicPlanetEngine`**: Maps raw astronomical planets to placed `ChartPlanet` objects.
- **`VedicHouseEngine`**: Formats house cusps and occupant mappings.
- **`VedicHouseLordEngine`**: Calculates sign ownership and house lord placements.
- **`VedicDrishtiEngine`**: Calculates Graha Drishti aspects (7th full aspect + Mars 4/8, Jupiter 5/9, Saturn 3/10).
- **`VedicStrengthEngine`**: Evaluates dignities, combustion, retrograde, and planet strength scores.
