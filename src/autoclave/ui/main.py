import logging

from autoclave.ui.window.main_window import InterfazPrincipal
from autoclave.ui.service_ui.backend_client import BackendClient
from autoclave.ui.service_ui.ui_service_backend import UIServiceBackend
from autoclave.services.domain.puertas.door_command_service import DoorCommandService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # IP FIJA DEL BACKEND (PC de la máquina)
    backend = BackendClient("http://192.168.100.10:8000")

    # Servicios de UI
    ui_service = UIServiceBackend(backend)
    door_commands = DoorCommandService(
        backend_client=backend,
        source_door=1,   # ESTA PANTALLA (UI)
    )

    # Lanzar UI
    app = InterfazPrincipal(
        ui_service=ui_service,
        door_commands=door_commands,
    )

    logger.info("🖥️ UI Autoclave iniciada")
    app.mainloop()


if __name__ == "__main__":
    main()