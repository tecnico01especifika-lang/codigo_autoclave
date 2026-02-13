# autoclave/backend/context.py

from autoclave.core.status import EstadoAutoclave
from autoclave.services.domain.puertas.ser_puertas import ServicioPuertas
from autoclave.installation.bootstrap import get_installation_profile
from autoclave.devices.factory.factory import build_hardware
from autoclave.devices.puertas.door import Door
from autoclave.devices.io.set_io import SetOutput
from autoclave.services.domain.loop.control_loop import ControlLoop
from autoclave.state_machine.alarms.alarm_manager import AlarmManager

import logging

logger = logging.getLogger(__name__)


class BackendContext:
    def __init__(self):
        self.estado = EstadoAutoclave()
        self.alarm_manager = AlarmManager(self.estado)
        self.profile = get_installation_profile()
        if self.profile is None:
            raise RuntimeError("Backend sin InstallationProfile")


        # Hardware real
        self.units, self.serial, doors_cfg = build_hardware()

        self.setdo = SetOutput(self.serial, self.estado)

        self.doors = [
            Door(
                name=cfg["name"],
                di=cfg["di"],
                do=cfg["do"],
                ai=cfg["ai"],
                estado=self.estado,
                setdo=self.setdo,
            )
            for cfg in doors_cfg
        ]

        # Servicio de dominio (ÚNICO)
        self.servicio_puertas = ServicioPuertas(
            doors=self.doors,
            estado=self.estado,
            profile=self.profile,
            logger=logger,
        )

        self.control_loop = ControlLoop(
            units=self.units,
            door_service=self.servicio_puertas,
            doors=self.doors,
            estado=self.estado,
            link=self.serial,
            set_do=self.setdo,
            alarm_manager=self.alarm_manager,
        )
        self.control_loop.start()