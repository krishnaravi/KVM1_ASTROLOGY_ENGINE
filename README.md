# KVM1 Astrology Engine

FastAPI service computing **sidereal (Lahiri) Vedic charts** from the Swiss
Ephemeris, with Parashari interpretation layered on top: house lords, graha
drishti, planetary dignities, strength scores and yogas.

---

## Running

Requires **Python 3.12+**.

```bash
python -m venv .venv
.venv/Scripts/activate          # Windows;  source .venv/bin/activate on POSIX
pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive docs at `http://127.0.0.1:8000/docs`.

> Run from the **repository root** — modules import via absolute paths
> (`core.constants`, `services.…`), so the root must be on `sys.path`.

---

## API

All chart endpoints take `date` (`YYYY-MM-DD`) and `time` (`HH:MM`).

| Method | Path | Query params | Returns |
|---|---|---|---|
| GET | `/` | — | engine banner |
| GET | `/health` | — | `{"status": "healthy"}` |
| GET | `/api/lagna` | `date, time, latitude, longitude` | ascendant longitude, sign, degree-in-sign |
| GET | `/api/planet-positions` | `date, time` | 9 grahas: longitude, latitude, speed, retrograde, sign, nakshatra, pada |
| GET | `/api/houses` | `date, time, latitude, longitude` | 12 Placidus cusps with sign + degree |
| GET | `/api/rasi-chart` | `date, time, latitude, longitude` | full chart (see below) |
| GET | `/calculate-horoscope` | `date_str, time_str` | **legacy** — sun/moon sign only; superseded by `/api/planet-positions` |

`/api/rasi-chart` response keys: `houses`, `house_lords`,
`house_lord_positions`, `house_occupants`, `conjunctions`, `graha_drishti`,
`yogas`, `planet_strengths`, `planet_scores`, `planets`.

---

## Architecture

Calculation flows one direction; each stage only reads what earlier stages produced.

```
date/time/lat/lon
  → planet_service          Swiss Ephemeris → Planet (raw astronomy only)
  → house_service           → house_systems/placidus → 12 cusps
  → ChartPlanet             raw Planet + house number
  → house_lord_service      sign → Parashari lord
  → house_lord_position_service
  → house_occupants_service
  → conjunction_service
  → drishti/graha_drishti
  → yogas/yoga_engine       runs YOGA_RULES
  → strengths/strength_engine  one dignity + combustion + retrograde
  → score_engine            max(positive) − sum(negative), floored at 0
  → analyzers/planet_analyzer  writes dignity + strength_score onto ChartPlanet
  → ChartPipeline.build()
```

### Layout

| Path | Role |
|---|---|
| `core/` | zodiac + planet constants, nakshatra maths, Julian Day |
| `domain/` | `Planet` (raw — never carries house/dignity), `ChartPlanet` (placed) |
| `routers/` | HTTP layer, one module per resource |
| `services/` | orchestration + one service per concern |
| `services/config/dignities.py` | exaltation / debilitation / own / moolatrikona / friend / neutral / enemy / combustion tables |
| `services/house_systems/` | `placidus.py` (active), `whole_sign.py` (written, not wired) |
| `services/strengths/` | one file per strength rule + `strength_engine.py` |
| `services/yogas/` | one file per yoga rule + `yoga_engine.py` |
| `tests/` | golden-chart regression suite |

---

## Adding a rule

Both engines are plain dispatchers — a new rule is one file plus one list entry.

**Yoga.** Write `services/yogas/<name>.py` exposing
`check(chart) -> dict | list[dict] | None`, then append it to `YOGA_RULES` in
`services/yogas/yoga_engine.py`. `chart` gives you `planets`,
`house_lord_positions`, `house_occupants`, `conjunctions`, `graha_drishti` and
`houses`. Build the return value with `services.yogas.base.make_yoga()`.

**Strength.** Write `services/strengths/<name>.py` exposing
`check(chart) -> list[dict]` with keys `planet`, `strength`, `score`, `reason`.
Register it in `strength_engine.py` under either `DIGNITY_RULES` (mutually
exclusive — the first match per planet wins, so **order matters**) or
`OTHER_RULES` (can stack).

Keep the numeric tables in `services/config/`, not in the rule module.

---

## Tests

Golden-chart regression suite — stdlib `unittest`, no extra dependencies:

```bash
python -m unittest discover -s tests -v
```

Run from the repository root (39 tests, ~0.6 s).

It pins the serialised response of every endpoint across 7 fixture charts plus
the generated OpenAPI schema. Any change to chart output or to the API contract
fails the suite. Regenerate the golden file **only** with a deliberate,
approved behaviour change:

```bash
python tests/generate_golden.py
```

---

## Conventions

- **Ayanamsa:** Lahiri (`swe.SIDM_LAHIRI`), sidereal.
- **House system:** Placidus. Degrades above ~66° latitude; `whole_sign.py`
  exists as an alternative but is not currently wired in.
- **Sign names** are Tamil strings and act as the join key between the house,
  lord and dignity tables. The single source of truth is
  `core.constants.ZODIAC_SIGNS` — never re-declare the list locally.
- **Ephemeris:** no explicit ephemeris path is set, so pyswisseph falls back to
  its built-in Moshier model (arc-second accuracy).
