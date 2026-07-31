from services.planet_service import get_all_planets
from services.house_service import get_houses
from services.house_lord_service import get_house_lords
from services.house_lord_position_service import get_house_lord_positions
from services.house_occupants_service import get_house_occupants
from services.conjunction_service import get_conjunctions
from services.chart_pipeline import ChartPipeline
from domain.chart import ChartPlanet


def get_planet_house(planet_longitude, houses):
    for house in houses:
        start = house["longitude"]

        if house["house"] == 12:
            end = houses[0]["longitude"] + 360
        else:
            end = houses[house["house"]]["longitude"]

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

    planets = get_all_planets(date, time)

    houses = get_houses(
        date,
        time,
        latitude,
        longitude,
    )

    house_lords = get_house_lords(houses)

    chart_planets = []

    for planet in planets:
        chart_planets.append(
            ChartPlanet(
                name=planet.name,
                longitude=planet.longitude,
                sign=planet.sign,
                degree_in_sign=planet.degree_in_sign,
                house=get_planet_house(
                    planet.longitude,
                    houses,
                ),
                nakshatra=planet.nakshatra,
                nakshatra_lord=planet.nakshatra_lord,
                pada=planet.pada,
            )
        )

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

    pipeline.add("houses", houses)
    pipeline.add("house_lords", house_lords)
    pipeline.add("house_lord_positions", house_lord_positions)
    pipeline.add("house_occupants", house_occupants)
    pipeline.add("conjunctions", conjunctions)
    pipeline.add("planets", chart_planets)

    return pipeline.build()