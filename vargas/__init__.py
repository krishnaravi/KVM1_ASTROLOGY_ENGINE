"""
Divisional Charts (Vargas) Engine Package.
"""

from vargas.base import IVargaCalculator
from vargas.registry import VargaRegistry, varga_registry, bootstrap_vargas

__all__ = [
    "IVargaCalculator",
    "VargaRegistry",
    "varga_registry",
    "bootstrap_vargas",
]
