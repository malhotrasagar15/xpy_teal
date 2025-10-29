# src/xpy_teal/__init__.py

# Import modules from Codes
from .Codes import (
    spectrum_tools,
    math_tools,
    dataIO,
    line_analysis,
    xpy_teal_pipeline,
    download_xp_spectra,
    config
)

# Import constants from config
from .Codes.config import DATA_DIR, CONFIG_DIR

__all__ = [
    "spectrum_tools",
    "math_tools",
    "dataIO",
    "line_analysis",
    "xpy_teal_pipeline",
    "download_xp_spectra",
    "DATA_DIR",
    "CONFIG_DIR",
]
