# Phase 6 Architecture: Divisional Charts (Varga) Engine

## Overview

Phase 6 implements the 14 Parashari Divisional Chart (Varga) Calculators and `VargaRegistry`.

```
                      +-----------------------------+
                      |     CalculationContext      |
                      |  (Single Source of Truth)   |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |        VargaRegistry        |
                      +--------------+--------------+
                                     |
        +-------+-------+-------+----+----+-------+-------+-------+
        |       |       |       |         |       |       |       |
        v       v       v       v         v       v       v       v
      [D2]    [D3]    [D7]    [D9]      [D10]   [D12]   [D16]   [D20]
      Hora   Drekk. Sapt.   Navamsa    Dasamsa Dwadas. Shodas. Vims.

        +-------+-------+-------+----+----+
        |       |       |       |         |
        v       v       v       v         v
      [D24]   [D27]   [D30]   [D40]     [D45]   [D60]
      Chat.   Bhamsa  Trims.  Khaved.   Aksha.  Shastiamsa
```

## Varga Taxonomy Table

| Code | Name | Division Size | Primary Focus |
|---|---|---|---|
| **D2** | Hora | 15°00' | Wealth & Prosperity |
| **D3** | Drekkana | 10°00' | Siblings & Courage |
| **D7** | Saptamsa | 4°17'08" | Children & Progeny |
| **D9** | Navamsa | 3°20' | Spouse, Dharma & General Fortune |
| **D10** | Dasamsa | 3°00' | Career, Profession & Karma |
| **D12** | Dwadasamsa | 2°30' | Parents & Ancestry |
| **D16** | Shodasamsa | 1°52'30" | Vehicles & Luxuries |
| **D20** | Vimsamsa | 1°30' | Spiritual Progress & Upasana |
| **D24** | Chaturvimsamsa | 1°15' | Higher Learning & Knowledge |
| **D27** | Bhamsa | 1°06'40" | Strengths & Vulnerabilities |
| **D30** | Trimsamsa | Irregular | Misfortunes & Evils |
| **D40** | Khavedamsa | 0°45' | Auspicious Effects & Lineage |
| **D45** | Akshavedamsa | 0°40' | General Character & Integrity |
| **D60** | Shastiamsa | 0°30' | Past Life Karma & Root Causes |
