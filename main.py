from fastapi import FastAPI
from core.constants import ZODIAC_SIGNS
from routers.lagna import router as lagna_router
from routers.health import router as health_router
from routers.planet import router as planet_router
from routers.house import router as house_router
from routers.chart import router as chart_router
app = FastAPI(
    title="KVM1 Astrology Engine",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "engine": "KVM1",
        "status": "running"
    }
from fastapi.middleware.cors import CORSMiddleware
import swisseph as swe

from core.swisseph_service import get_julian_day



# வேர்ட்பிரஸ் தளத்திலிருந்து தரவுகள் வர அனுமதி அளித்தல் (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(lagna_router)
app.include_router(health_router)
app.include_router(planet_router)
app.include_router(house_router)
app.include_router(chart_router)

# லஹிரி அயனாம்ச முறை core.swisseph_service இறக்குமதியின்போது
# ஒரே முறை அமைக்கப்படுகிறது.

@app.get("/calculate-horoscope")
def calculate_horoscope(date_str: str, time_str: str):
    try:
        # 1-2. தேதி/நேரத்தை ஜூலியன் நாளாக மாற்றுதல்
        # (core.swisseph_service இல் உள்ள ஒரே நியமன செயலி)
        julian_day = get_julian_day(date_str, time_str)

        # 3. சூரியன் மற்றும் சந்திரனின் நிலைகளை 'நிராயண' (Sidereal) இந்திய முறையில் கணக்கிடுதல்
        # சூரியன் (SE_SUN = 0)
        sun_res, _ = swe.calc_ut(julian_day, swe.SUN, swe.FLG_SIDEREAL)
        sun_deg = sun_res[0]
        
        # சந்திரன் (SE_MOON = 1)
        moon_res, _ = swe.calc_ut(julian_day, swe.MOON, swe.FLG_SIDEREAL)
        moon_deg = moon_res[0]
        
        # 4. ராசிப் பெயர்களின் பட்டியல் (core.constants இலிருந்து)
        sun_sign = ZODIAC_SIGNS[int(sun_deg // 30)]
        moon_sign = ZODIAC_SIGNS[int(moon_deg // 30)]
        
        # விடைகளை வேர்ட்பிரஸிற்கு JSON ஆக அனுப்புதல்
        return {
            "status": "success",
            "date": date_str,
            "time": time_str,
            "sun_longitude": round(sun_deg, 2),
            "sun_sign": sun_sign,
            "moon_longitude": round(moon_deg, 2),
            "moon_sign": moon_sign
        }
        
    except Exception as e:
        return {"status": "error", "message": str(e)}