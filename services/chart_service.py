from services.planet_service import get_all_planets
from services.house_service import get_houses
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
    longitude: float
):
    planets = get_all_planets(date, time)

    houses = get_houses(
        date,
        time,
        latitude,
        longitude
    )

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
                    houses
                ),
                nakshatra=planet.nakshatra,
                nakshatra_lord=planet.nakshatra_lord,
                pada=planet.pada
            )
        )

    return {
        "houses": houses,
        "planets": chart_planets
    }