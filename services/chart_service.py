from domain.chart import ChartPlanet

from services.planet_service import get_all_planets
from services.house_service import get_houses
from services.house_lord_service import get_house_lords
from services.house_lord_position_service import get_house_lord_positions
from services.house_occupants_service import get_house_occupants
from services.conjunction_service import get_conjunctions
from services.chart_pipeline import ChartPipeline
from services.drishti.graha_drishti import get_graha_drishti
from services.yogas.yoga_engine import get_yogas
from services.strengths.strength_engine import get_strengths
from services.score_engine import build_scores
from services.analyzers.planet_analyzer import analyze


def get_planet_house(planet_longitude, houses):

    for i, house in enumerate(houses):

        start = house["longitude"]

        if i == len(houses) - 1:
            end = houses[0]["longitude"] + 360
        else:
            end = houses[i + 1]["longitude"]

        lon = planet_longitude

        if lon < start:
            lon += 360

        if start <= lon < end:
            return house["house"]

    return 0


def build_rasi_chart(
    date: str,
    time: str,
    latitude: float,
    longitude: float,
):

    pipeline = ChartPipeline()

    # --------------------------------------------------
    # Raw Planet Data
    # --------------------------------------------------

    raw_planets = get_all_planets(
        date,
        time,
    )

    houses = get_houses(
        date,
        time,
        latitude,
        longitude,
    )

    # --------------------------------------------------
    # Convert Planet -> ChartPlanet
    # --------------------------------------------------

    chart_planets = []

    for p in raw_planets:

        chart_planets.append(

            ChartPlanet(

                name=p.name,

                longitude=p.longitude,
                latitude=p.latitude,
                speed=p.speed,
                retrograde=p.retrograde,

                sign=p.sign,
                degree_in_sign=p.degree_in_sign,

                house=get_planet_house(
                    p.longitude,
                    houses,
                ),

                nakshatra=p.nakshatra,
                nakshatra_lord=p.nakshatra_lord,
                pada=p.pada,

            )

        )

    # --------------------------------------------------
    # House Data
    # --------------------------------------------------

    house_lords = get_house_lords(houses)

    house_lord_positions = get_house_lord_positions(
        house_lords,
        chart_planets,
    )

    house_occupants = get_house_occupants(
        chart_planets,
    )

    conjunctions = get_conjunctions(
        house_occupants,
    )

    graha_drishti = get_graha_drishti(
        chart_planets,
    )

    # --------------------------------------------------
    # Chart Object
    # --------------------------------------------------

    chart = {

        "houses": houses,

        "house_lords": house_lords,

        "house_lord_positions": house_lord_positions,

        "house_occupants": house_occupants,

        "conjunctions": conjunctions,

        "graha_drishti": graha_drishti,

        "planets": chart_planets,

    }

    # --------------------------------------------------
    # Yogas
    # --------------------------------------------------

    yogas = get_yogas(chart)

    chart["yogas"] = yogas

    # --------------------------------------------------
    # Planet Strengths
    # --------------------------------------------------

    strengths = get_strengths(chart)

    chart["planet_strengths"] = strengths

    # --------------------------------------------------
    # Planet Scores
    # --------------------------------------------------

    planet_scores = build_scores(strengths)

    chart["planet_scores"] = planet_scores

    # --------------------------------------------------
    # Planet Analyzer
    # --------------------------------------------------

    chart_planets = analyze(
        chart_planets,
        strengths,
        planet_scores,
    )

    # IMPORTANT
    chart["planets"] = chart_planets

    # --------------------------------------------------
    # Pipeline
    # --------------------------------------------------

    pipeline.add("houses", houses)

    pipeline.add("house_lords", house_lords)

    pipeline.add(
        "house_lord_positions",
        house_lord_positions,
    )

    pipeline.add(
        "house_occupants",
        house_occupants,
    )

    pipeline.add(
        "conjunctions",
        conjunctions,
    )

    pipeline.add(
        "graha_drishti",
        graha_drishti,
    )

    pipeline.add(
        "yogas",
        yogas,
    )

    pipeline.add(
        "planet_strengths",
        strengths,
    )

    pipeline.add(
        "planet_scores",
        planet_scores,
    )

    pipeline.add(
        "planets",
        chart_planets,
    )

    return pipeline.build()