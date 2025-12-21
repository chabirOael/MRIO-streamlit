"""
Source package for MRIO emissions decomposition analysis.
"""
from .data_loader import load_S_L, build_catalog
from .computations import compute_direct_domestic_foreign
from .visualization import create_enhanced_donut, fmt_kg, percent
from .ui_components import show_welcome_message, show_footer

__all__ = [
    'load_S_L',
    'build_catalog',
    'compute_direct_domestic_foreign',
    'create_enhanced_donut',
    'fmt_kg',
    'percent',
    'show_welcome_message',
    'show_footer',
]

