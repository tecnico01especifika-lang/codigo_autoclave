# autoclave/services/ui/ui_service.py


from autoclave.state_machine.machine.eum_global import GlobalState

class UIService:
    def __init__(self, estado):
        self.estado = estado

    # ==============================
    # SENSORES
    # ==============================

    def get_sensores_temp(self):
        return dict(self.estado.sensores_temp)

    def get_sensores_pres(self):
        return dict(self.estado.sensores_pres)

    def get_sensores_di(self):
        return dict(self.estado.sensores_di)

    # ==============================
    # ALARMAS
    # ==============================

    def get_alarmas(self):
        #print("UI Service - Alarmas activas:", self.estado.Alarmas_activas)
        return list(self.estado.Alarmas_activas)

    # ==============================
    # ESTADO GLOBAL
    # ==============================

    def get_estado_global(self) -> GlobalState:
        return self.estado.get_machine_state()

    # ==============================
    # PUERTAS
    # ==============================

    def get_estado_puertas(self):
        return dict(self.estado.estado_puertas)

    def get_estado_puerta(self, nombre_puerta):
        return self.estado.get_door_state(nombre_puerta)
