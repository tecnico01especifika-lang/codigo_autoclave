# autoclave/services/ui/ui_service_backend.py

class UIServiceBackend:
    def __init__(self, backend_client):
        self.backend = backend_client
        self._cache = {}

    def _update(self):
        self._cache = self.backend.get_status()

    # ==============================
    # SENSORES
    # ==============================

    def get_sensores_temp(self):
        self._update()
        temp = self._cache.get("sensors", {}).get("temperature", {})
        return {
            "temp_camara": temp.get("camara"),
            "temp_ref": temp.get("ref"),
            "temp_chaqueta": temp.get("chaqueta"),
        }

    def get_sensores_pres(self):
        self._update()
        pres = self._cache.get("sensors", {}).get("pressure", {})
        return {
            "pres_camara": pres.get("camara"),
            "pres_chaqueta": pres.get("chaqueta"),
        }

    def get_sensores_di(self):
        self._update()
        return self._cache.get("sensors", {}).get("digital_inputs", {})

    # ==============================
    # ALARMAS
    # ==============================

    def get_alarmas(self):
        self._update()
        return self._cache.get("alarms", [])

    # ==============================
    # ESTADO GLOBAL
    # ==============================

    def get_estado_global(self):
        self._update()
        return self._cache.get("machine_state", "DESCONOCIDO")

    # ==============================
    # PUERTAS
    # ==============================

    def get_estado_puertas(self):
        self._update()
        return self._cache.get("doors", {})

    def get_estado_puerta(self, nombre_puerta):
        self._update()
        return self._cache.get("doors", {}).get(nombre_puerta)
