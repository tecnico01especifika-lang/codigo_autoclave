"""
autoclave.core.converters
-------------------------
Convierte señales crudas (ADC) a unidades físicas y aplica calibración y suavizado.
"""

from typing import List, Dict
from src.autoclave.config.schema import CalibrationConfig

_prev_temp_values: List[float] = [0.0] * 8
_prev_pres_values: List[float] = [0.0] * 8
SMOOTHING_FACTOR = 0.7


def _smooth(previous: float, new_value: float) -> float:
    return SMOOTHING_FACTOR * previous + (1 - SMOOTHING_FACTOR) * new_value


def _apply_calibration(raw_value: int, calib, full_scale: float) -> float:
    """Aplica la escala ADC y la calibración."""
    value = (raw_value / 4095.0) * full_scale
    gain = calib.gain if calib else 1.0
    offset = calib.offset if calib else 0.0
    return value * gain + offset


def convert_temperatures(raw_ai: List[int], config: Dict | CalibrationConfig) -> List[float]:
    if isinstance(config, dict):
        calib_list = config.get("calibration", {}).get("temperature", [])
    else:
        calib_list = config.calibration.temperature

    global _prev_temp_values
    temps = []
    for i in range(8):
        raw = raw_ai[i] if i < len(raw_ai) else 0
        calib = calib_list[i] if i < len(calib_list) else None
        value = _apply_calibration(raw, calib, 200.0)
        value = _smooth(_prev_temp_values[i], value)
        _prev_temp_values[i] = value
        temps.append(round(value, 2))
    return temps


def convert_pressures(raw_ai: List[int], config: Dict | CalibrationConfig) -> List[float]:
    if isinstance(config, dict):
        calib_list = config.get("calibration", {}).get("pressure", [])
    else:
        calib_list = config.calibration.pressure

    global _prev_pres_values
    press = []
    for i in range(8):
        raw = raw_ai[8 + i] if 8 + i < len(raw_ai) else 0
        calib = calib_list[i] if i < len(calib_list) else None
        value = _apply_calibration(raw, calib, 400.0)
        value = _smooth(_prev_pres_values[i], value)
        _prev_pres_values[i] = value
        press.append(round(value, 2))
    return press
