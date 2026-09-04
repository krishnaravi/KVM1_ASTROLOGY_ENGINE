from services.house_systems.placidus import calculate as calculate_placidus


def get_houses(
    date_str: str,
    time_str: str,
    latitude: float,
    longitude: float,
    timezone: float = 0.0,
):
    """
    Backward-compatible wrapper.

    Existing modules can continue calling get_houses(),
    while the actual calculation is delegated to the
    Placidus House System module.
    """

    return calculate_placidus(
        date_str=date_str,
        time_str=time_str,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
    )