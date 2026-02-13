"""
autoclave.config.schema
-----------------------
Define la estructura de configuración global del sistema,
incluyendo calibraciones, límites y parámetros generales.
"""

from pydantic import BaseModel, Field, confloat
from typing import List, Optional


# ---------------------------------------------------------------------
# Calibración de sensores (ya existente)
# ---------------------------------------------------------------------
class SensorCalibration(BaseModel):
    """Configuración individual de calibración para un canal."""
    offset: float = Field(0.0, description="Desplazamiento del sensor")
    gain: float = Field(1.0, description="Ganancia o factor de escala")
    poly: Optional[List[float]] = Field(None, description="Coeficientes polinomiales opcionales")


class CalibrationConfig(BaseModel):
    """Agrupa calibraciones por tipo de sensor."""
    temperature: List[SensorCalibration] = Field(default_factory=lambda: [SensorCalibration() for _ in range(8)])
    pressure: List[SensorCalibration] = Field(default_factory=lambda: [SensorCalibration() for _ in range(8)])

# ---------------------------------------------------------------------
# Configuración principal
# ---------------------------------------------------------------------
class AppConfig(BaseModel):
    """Configuración global del autoclave."""
    calibration: CalibrationConfig = Field(default_factory=CalibrationConfig)
    name: str = "Autoclave Principal"
    sampling_interval_ms: int = Field(
        500,
        ge=100, le=5000,
        description="Intervalo de muestreo en milisegundos (100–5000 ms)"
    )
