import yaml
from pathlib import Path
from autoclave.config.schema import AppConfig

def load_config(calibration_path: str | Path) -> AppConfig:
    """
    Carga y valida las configuraciones YAML del autoclave.
    Combina parámetros globales y de calibración en un único AppConfig.
    """
    calibration_path = Path(calibration_path)

    with open(calibration_path, "r", encoding="utf-8") as f:
        calibration_data = yaml.safe_load(f) or {}

    # Combinar ambas configuraciones en un solo dict
    merged = {
        "calibration": calibration_data
    }

    return AppConfig(**merged)

