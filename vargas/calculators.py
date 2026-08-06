"""
Implementations of the 14 Parashari Divisional Chart (Varga) Calculators.
"""

from typing import Tuple
from core.constants import ZODIAC_SIGNS
from vargas.base import IVargaCalculator


class D2HoraCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D2"
    @property
    def varga_name(self) -> str: return "Hora"
    @property
    def division_factor(self) -> int: return 2

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        is_odd = (rashi_idx % 2 == 0)

        # 0-15°: Sun (Leo=4) in odd, Moon (Cancer=3) in even
        # 15-30°: Moon (Cancer=3) in odd, Sun (Leo=4) in even
        if is_odd:
            target_idx = 4 if deg < 15.0 else 3
        else:
            target_idx = 3 if deg < 15.0 else 4

        v_deg = (deg % 15.0) * 2.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D3DrekkanaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D3"
    @property
    def varga_name(self) -> str: return "Drekkana"
    @property
    def division_factor(self) -> int: return 3

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part = int(deg // 10.0)

        if part == 0:
            target_idx = rashi_idx
        elif part == 1:
            target_idx = (rashi_idx + 4) % 12
        else:
            target_idx = (rashi_idx + 8) % 12

        v_deg = (deg % 10.0) * 3.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D7SaptamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D7"
    @property
    def varga_name(self) -> str: return "Saptamsa"
    @property
    def division_factor(self) -> int: return 7

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 30.0 / 7.0
        part = int(deg // part_size)

        is_odd = (rashi_idx % 2 == 0)
        start_sign = rashi_idx if is_odd else (rashi_idx + 6) % 12
        target_idx = (start_sign + part) % 12

        v_deg = (deg % part_size) * 7.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D9NavamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D9"
    @property
    def varga_name(self) -> str: return "Navamsa"
    @property
    def division_factor(self) -> int: return 9

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 30.0 / 9.0
        part = int(deg // part_size)

        element = rashi_idx % 4
        if element == 0:    # Fiery (Aries, Leo, Sag) -> Aries (0)
            start_sign = 0
        elif element == 1:  # Earthy (Taurus, Virgo, Cap) -> Cap (9)
            start_sign = 9
        elif element == 2:  # Airy (Gemini, Libra, Aqu) -> Libra (6)
            start_sign = 6
        else:               # Watery (Cancer, Scorpio, Pis) -> Cancer (3)
            start_sign = 3

        target_idx = (start_sign + part) % 12
        v_deg = (deg % part_size) * 9.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D10DasamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D10"
    @property
    def varga_name(self) -> str: return "Dasamsa"
    @property
    def division_factor(self) -> int: return 10

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 3.0
        part = int(deg // part_size)

        is_odd = (rashi_idx % 2 == 0)
        start_sign = rashi_idx if is_odd else (rashi_idx + 9) % 12
        target_idx = (start_sign + part) % 12

        v_deg = (deg % part_size) * 10.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D12DwadasamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D12"
    @property
    def varga_name(self) -> str: return "Dwadasamsa"
    @property
    def division_factor(self) -> int: return 12

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 2.5
        part = int(deg // part_size)

        target_idx = (rashi_idx + part) % 12
        v_deg = (deg % part_size) * 12.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D16ShodasamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D16"
    @property
    def varga_name(self) -> str: return "Shodasamsa"
    @property
    def division_factor(self) -> int: return 16

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 30.0 / 16.0
        part = int(deg // part_size)

        modality = rashi_idx % 3
        if modality == 0:   # Movable (Aries=0)
            start_sign = 0
        elif modality == 1: # Fixed (Leo=4)
            start_sign = 4
        else:               # Dual (Sag=8)
            start_sign = 8

        target_idx = (start_sign + part) % 12
        v_deg = (deg % part_size) * 16.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D20VimsamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D20"
    @property
    def varga_name(self) -> str: return "Vimsamsa"
    @property
    def division_factor(self) -> int: return 20

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 1.5
        part = int(deg // part_size)

        modality = rashi_idx % 3
        if modality == 0:   # Movable -> Aries (0)
            start_sign = 0
        elif modality == 1: # Fixed -> Sag (8)
            start_sign = 8
        else:               # Dual -> Leo (4)
            start_sign = 4

        target_idx = (start_sign + part) % 12
        v_deg = (deg % part_size) * 20.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D24ChaturvimsamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D24"
    @property
    def varga_name(self) -> str: return "Chaturvimsamsa"
    @property
    def division_factor(self) -> int: return 24

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 1.25
        part = int(deg // part_size)

        is_odd = (rashi_idx % 2 == 0)
        start_sign = 4 if is_odd else 3  # Leo in odd, Cancer in even
        target_idx = (start_sign + part) % 12

        v_deg = (deg % part_size) * 24.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D27BhamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D27"
    @property
    def varga_name(self) -> str: return "Bhamsa"
    @property
    def division_factor(self) -> int: return 27

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 30.0 / 27.0
        part = int(deg // part_size)

        element = rashi_idx % 4
        if element == 0:    # Fiery -> Aries (0)
            start_sign = 0
        elif element == 1:  # Earthy -> Cancer (3)
            start_sign = 3
        elif element == 2:  # Airy -> Libra (6)
            start_sign = 6
        else:               # Watery -> Capricorn (9)
            start_sign = 9

        target_idx = (start_sign + part) % 12
        v_deg = (deg % part_size) * 27.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D30TrimsamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D30"
    @property
    def varga_name(self) -> str: return "Trimsamsa"
    @property
    def division_factor(self) -> int: return 30

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        is_odd = (rashi_idx % 2 == 0)

        if is_odd:
            if deg < 5.0:
                target_idx, span = 0, 5.0   # Mars (Aries)
            elif deg < 10.0:
                target_idx, span = 10, 5.0  # Saturn (Aquarius)
            elif deg < 18.0:
                target_idx, span = 8, 8.0   # Jupiter (Sagittarius)
            elif deg < 25.0:
                target_idx, span = 2, 7.0   # Mercury (Gemini)
            else:
                target_idx, span = 6, 5.0   # Venus (Libra)
        else:
            if deg < 5.0:
                target_idx, span = 1, 5.0   # Venus (Taurus)
            elif deg < 12.0:
                target_idx, span = 5, 7.0   # Mercury (Virgo)
            elif deg < 20.0:
                target_idx, span = 11, 8.0  # Jupiter (Pisces)
            elif deg < 25.0:
                target_idx, span = 9, 5.0   # Saturn (Capricorn)
            else:
                target_idx, span = 7, 5.0   # Mars (Scorpio)

        v_deg = (deg % span) * (30.0 / span)
        return ZODIAC_SIGNS[target_idx], v_deg


class D40KhavedamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D40"
    @property
    def varga_name(self) -> str: return "Khavedamsa"
    @property
    def division_factor(self) -> int: return 40

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 0.75
        part = int(deg // part_size)

        is_odd = (rashi_idx % 2 == 0)
        start_sign = 0 if is_odd else 6  # Aries in odd, Libra in even
        target_idx = (start_sign + part) % 12

        v_deg = (deg % part_size) * 40.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D45AkshavedamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D45"
    @property
    def varga_name(self) -> str: return "Akshavedamsa"
    @property
    def division_factor(self) -> int: return 45

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 30.0 / 45.0
        part = int(deg // part_size)

        modality = rashi_idx % 3
        if modality == 0:   # Movable -> Aries (0)
            start_sign = 0
        elif modality == 1: # Fixed -> Leo (4)
            start_sign = 4
        else:               # Dual -> Sag (8)
            start_sign = 8

        target_idx = (start_sign + part) % 12
        v_deg = (deg % part_size) * 45.0
        return ZODIAC_SIGNS[target_idx], v_deg


class D60ShastiamsaCalculator(IVargaCalculator):
    @property
    def varga_code(self) -> str: return "D60"
    @property
    def varga_name(self) -> str: return "Shastiamsa"
    @property
    def division_factor(self) -> int: return 60

    def calculate_varga_sign(self, longitude: float) -> Tuple[str, float]:
        rashi_idx = int(longitude // 30) % 12
        deg = longitude % 30
        part_size = 0.5
        part = int(deg // part_size)

        target_idx = (rashi_idx + part) % 12
        v_deg = (deg % part_size) * 60.0
        return ZODIAC_SIGNS[target_idx], v_deg
