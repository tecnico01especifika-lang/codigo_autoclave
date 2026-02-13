# autoclave/backend/server.py



from fastapi import HTTPException, FastAPI, Body
from autoclave.backend.context import BackendContext

app = FastAPI(title="Autoclave Backend")

context = BackendContext()

@app.get("/status", response_model=None)
def get_status():
    estado = context.estado

    # ------------------------------
    # ESTADO DE LA MÁQUINA
    # ------------------------------
    machine_state = None
    try:
        machine_state = estado.get_machine_state().name
    except Exception:
        machine_state = "DESCONOCIDO"

    # ------------------------------
    # ESTADO DE PUERTAS
    # ------------------------------
    doors = {
        door_name: door_state.name
        for door_name, door_state in estado.estado_puertas.items()
    }

    # ------------------------------
    # SENSORES
    # ------------------------------
    sensors = {
        "temperature": {
            "camara": estado.sensores_temp.get("temp_camara"),
            "ref": estado.sensores_temp.get("temp_ref"),
            "chaqueta": estado.sensores_temp.get("temp_chaqueta"),
        },
        "pressure": {
            "camara": estado.sensores_pres.get("pres_camara"),
            "chaqueta": estado.sensores_pres.get("pres_chaqueta"),
        },
        "digital_inputs": dict(estado.sensores_di),
    }

    # ------------------------------
    # ALARMAS
    # ------------------------------
    alarms = [
        {
            "id": alarma.id,
            "level": alarma.type.name,
        }
        for alarma in estado.Alarmas_activas
    ]

    # ------------------------------
    # RESPUESTA FINAL (DTO)
    # ------------------------------
    return {
        "machine_state": machine_state,
        "doors": doors,
        "sensors": sensors,
        "alarms": alarms,
    }

@app.post("/doors/{door_name}/open")
def open_door(door_name: str, body: dict = Body(...)):
    source_door = body.get("source_door")

    if not context.servicio_puertas.request_open(door_name):
        raise HTTPException(
            status_code=403,
            detail="Apertura de puerta no permitida"
        )

    return {
        "ok": True,
        "door": door_name,
        "action": "open",
        "source_door": source_door,
    }


@app.post("/doors/{door_name}/close")
def close_door(door_name: str, body: dict = Body(...)):
    source_door = body.get("source_door")

    if not context.servicio_puertas.request_close(door_name):
        raise HTTPException(
            status_code=403,
            detail="Cierre de puerta no permitido"
        )

    return {
        "ok": True,
        "door": door_name,
        "action": "close",
        "source_door": source_door,
    }
