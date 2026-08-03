ChartPlanet(

    name=planet.name,

    longitude=planet.longitude,
    latitude=planet.latitude,
    speed=planet.speed,
    retrograde=planet.retrograde,

    sign=planet.sign,
    degree_in_sign=planet.degree_in_sign,

    house=get_planet_house(
        planet.longitude,
        houses,
    ),

    nakshatra=planet.nakshatra,
    nakshatra_lord=planet.nakshatra_lord,
    pada=planet.pada,

    declination=0.0,

    dignity=None,
    strength_score=0,
)