"""
Swiss Ephemeris Service implementing ISwissephService and IPipelineStage.
Single Source of Truth for astronomical planetary & house calculations.
MUST NOT contain business rules or prediction logic.
"""

import time
import swisseph as swe
from typing import Tuple, List
from core.interfaces.pipeline_interface import IPipelineStage
from core.interfaces.swisseph_interface import ISwissephService
from core.constants import SIDEREAL_MODE, PLANETS, ZODIAC_SIGNS
from core.nakshatra import get_nakshatra
from domain.models.calculation_context import CalculationContext
from domain.models.ephemeris_context import EphemerisContext
from domain.models.astronomical_state import AstronomicalState
from domain.models.stage_metrics import PipelineStageMetrics
from domain.planet import Planet
from domain.house import House
from core.errors import SwissEphemerisError

# Initialize Lahiri Sidereal Mode
swe.set_sid_mode(SIDEREAL_MODE)


class SwissephService(ISwissephService, IPipelineStage):
    """
    Swiss Ephemeris wrapper service providing pure astronomical calculations.
    """

    @property
    def stage_id(self) -> str:
        return "STAGE_SWISS_EPHEMERIS"

    @property
    def stage_name(self) -> str:
        return "Swiss Ephemeris Astronomical Stage"

    def calc_planet(self, julian_day: float, planet_id: int) -> Tuple[float, float, float]:
        """
        Calculates raw sidereal longitude, latitude, and speed for a planet ID.
        """
        try:
            result, _ = swe.calc_ut(
                julian_day,
                planet_id,
                swe.FLG_SIDEREAL | swe.FLG_SPEED,
            )
            return float(result[0]), float(result[1]), float(result[3])
        except Exception as e:
            raise SwissEphemerisError(
                human_message=f"Swiss Ephemeris calc_ut failed for planet {planet_id}: {str(e)}"
            ) from e

    def get_ayanamsa(self, julian_day: float) -> float:
        """
        Retrieves current Lahiri ayanamsa value in degrees for a given Julian Day.
        """
        try:
            return float(swe.get_ayanamsa_ut(julian_day))
        except Exception as e:
            raise SwissEphemerisError(
                human_message=f"Swiss Ephemeris get_ayanamsa_ut failed for jd {julian_day}: {str(e)}"
            ) from e

    def get_ephemeris_version(self) -> str:
        """
        Returns Swiss Ephemeris library version string.
        """
        return "Swiss Ephemeris 2.10.03"

    def process(self, context: CalculationContext) -> CalculationContext:
        start_time = time.perf_counter()
        input_version = context.context_version

        if not context.julian_day_context or not context.resolved_location:
            raise SwissEphemerisError(
                human_message="Cannot execute Swiss Ephemeris: JulianDayContext or ResolvedLocation missing in context.",
                trace_id=context.trace_id,
                stage_id=self.stage_id,
            )

        jd = context.julian_day_context.julian_day
        loc = context.resolved_location

        try:
            ayanamsa_deg = self.get_ayanamsa(jd)
            eph_ctx = EphemerisContext(
                ephemeris_version=self.get_ephemeris_version(),
                ayanamsa_name="Lahiri",
                ayanamsa_value=round(ayanamsa_deg, 6),
            )

            # 1. Compute Planets
            planets: List[Planet] = []
            for name, planet_id in PLANETS.items():
                lon, lat, spd = self.calc_planet(jd, planet_id)
                sign = ZODIAC_SIGNS[int(lon // 30)]
                degree_in_sign = lon % 30
                nak = get_nakshatra(lon)

                planets.append(
                    Planet(
                        name=name,
                        longitude=round(lon, 6),
                        latitude=round(lat, 6),
                        speed=round(spd, 6),
                        retrograde=(spd < 0),
                        sign=sign,
                        degree_in_sign=round(degree_in_sign, 6),
                        nakshatra=nak["name"],
                        nakshatra_lord=nak["lord"],
                        pada=nak["pada"],
                    )
                )

            # Ketu Calculation (180 degrees opposite Rahu)
            rahu = next(p for p in planets if p.name == "Rahu")
            ketu_lon = (rahu.longitude + 180.0) % 360.0
            ketu_nak = get_nakshatra(ketu_lon)
            ketu_sign = ZODIAC_SIGNS[int(ketu_lon // 30)]

            planets.append(
                Planet(
                    name="Ketu",
                    longitude=round(ketu_lon, 6),
                    latitude=0.0,
                    speed=0.0,
                    retrograde=False,
                    sign=ketu_sign,
                    degree_in_sign=round(ketu_lon % 30, 6),
                    nakshatra=ketu_nak["name"],
                    nakshatra_lord=ketu_nak["lord"],
                    pada=ketu_nak["pada"],
                )
            )

            # 2. Compute Placidus Houses
            houses: List[House] = []
            # Placidus house system flag = b'P'
            cusps, ascmc = swe.houses_ex(jd, loc.latitude, loc.longitude, b'P', swe.FLG_SIDEREAL)
            for i in range(1, 13):
                h_lon = float(cusps[i - 1])
                h_sign = ZODIAC_SIGNS[int(h_lon // 30)]
                houses.append(
                    House(
                        number=i,
                        longitude=round(h_lon, 6),
                        sign=h_sign,
                    )
                )

            astronomical_state = AstronomicalState(
                julian_day=jd,
                ayanamsa_deg=round(ayanamsa_deg, 6),
                planets=planets,
                houses=houses,
                additional_data={"ascendant_longitude": round(float(ascmc[0]), 6)},
            )

        except Exception as e:
            if isinstance(e, SwissEphemerisError):
                e.trace_id = context.trace_id
                e.stage_id = self.stage_id
                raise e
            raise SwissEphemerisError(
                human_message=f"Swiss Ephemeris processing failed: {str(e)}",
                trace_id=context.trace_id,
                stage_id=self.stage_id,
            ) from e

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        metric = PipelineStageMetrics(
            stage_id=self.stage_id,
            stage_name=self.stage_name,
            input_context_version=input_version,
            output_context_version=input_version + 1,
            execution_time_ms=elapsed_ms,
            cache_hit=False,
            status="SUCCESS",
        )

        return context.with_enrichment(
            ephemeris_context=eph_ctx,
            astronomical_state=astronomical_state,
            new_metric=metric,
        )
