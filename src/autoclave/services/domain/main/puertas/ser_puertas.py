#empezaremos con la logica de automatizacion de puertas
#este modulo se encargara de coordinar y decidir cuando actuar sobre las puertas
#Ejemplo de responsabilidades:
#- abrir las puertas cuando la UI lo solicite
#- registrar eventos de apertura/cierre
#- verificar el estado de las puertas
#- manejar errores relacionados con las puertas
# esto evita que la UI controle hadware directamente, mejorando la modularidad
#rol: coordinador y guardian de reglas
#- recibe solicitudes de apertura/cierre desde la UI
#- valida si la accion es permitida segun el estado actual
#- llama a la puerta
#- registra eventos y errores
#- notifica a la UI sobre el resultado de las acciones
#- maneja politicas (seguridad, permisos, secuencias)
#no controla hardware directamente, delega en el modulo de puertas
#vive en el nivel de servicio, no en el nivel de dispositivo

import logging
from autoclave.core.status import estado
from autoclave.devices.puertas.door import Door,DoorState

logger = logging.getLogger(__name__)

class rules:
    PRESION_ATMOSFERICA = 100.0  # Presión atmosférica en kPa
    RANGO_PRES_ATM = 10.0  # Rango de tolerancia para considerar presión atmosférica


class ServicioPuertas:
    def __init__(self, doors, logger=logger):
        self.doors = doors
        self.logger = logger
        self._last_states = {door: None for door in doors}
        
        
    #============================
    #API HACIA LA INTERFAZ
    #============================
    
    def resquest_open(self, door_id):
        door = self.doors[door_id]
        if not self.can_open(door):
            self.logger.warning("Apertura de puerta denegada por condiciones de seguridad.")
            return False
        
        door.cmd_abrir()
        self.logger.info("Comando de apertura de puerta enviado.")
        return True

    def resquest_close(self, door_id):
        door = self.doors[door_id]
        if not self.can_close(door):
            self.logger.warning("Cierre de puerta denegado por condiciones de seguridad.")
            return False
        
        door.cmd_cerrar()
        self.logger.info("Comando de cierre de puerta enviado.")
        return True

    def get_status(self, door_index=None):
        # Devuelve el estado de las puertas.
        # - Si door_index=None: devuelve un dict {0: "CERRADO", 1: "ABIERTO", ...}
        # - Si door_index=int: devuelve el estado de esa puerta
        if door_index is None:
            return {i: door.state.name for i, door in enumerate(self.doors)}
        else:
            return self.doors[door_index].state.name

    
    #============================
    #REGLAS Y POLITICAS
    #============================
    
    def can_open(self, door):
        # Verifica si la puerta puede abrirse según las condiciones actuales
        if estado.sensores_pres["pres_camara"] > rules.PRESION_ATMOSFERICA + rules.RANGO_PRES_ATM:
            logger.warning("No se puede abrir la puerta: presión de cámara alta.")
            return False
        
        if estado.sensores_pres["pres_camara"] < rules.PRESION_ATMOSFERICA - rules.RANGO_PRES_ATM:
            logger.warning("No se puede abrir la puerta: presión de cámara baja.")
            return False
        
        if estado.sensores_temp["temp_camara"] > 120:
            logger.warning("No se puede abrir la puerta: temperatura de cámara alta.")
            return False
        
        #verifica si la otra puerta esta cerrada

        for d in self.doors:
            if d is not door and d.state != DoorState.CERRADO:
                logger.warning("No se puede abrir la puerta: otra puerta está abierta.")
                return False
        return True
    
    def can_close(self, door):
        # Verifica si la puerta puede cerrarse según las condiciones actuales
        # -que la presion de la camara este cerca de la atmosferica
        if estado.sensores_pres["pres_camara"] < rules.PRESION_ATMOSFERICA - rules.RANGO_PRES_ATM:
            logger.warning("No se puede cerrar la puerta: presión de cámara baja.")
            return False
        
        if estado.sensores_pres["pres_camara"] > rules.PRESION_ATMOSFERICA + rules.RANGO_PRES_ATM:
            logger.warning("No se puede cerrar la puerta: presión de cámara alta.")
            return False
        #-que la temperatura de la camara no sea alta
        if estado.sensores_temp["temp_camara"] > 120:
            logger.warning("No se puede cerrar la puerta: temperatura de cámara alta.")
            return False
        
        #-que la puerta no este ya cerrandose o cerrada
        if door.state in [DoorState.CERRANDO, DoorState.CERRADO]:
            return False
        
        # -que el empaque no este presurizado (la presion del empaque debe ser cercana a la atmosferica o menor)
        pres_empaque = estado.sensores_pres.get(f"pres_empaque_{door.name[-1]}")
        if pres_empaque is not None:
            if pres_empaque > rules.PRESION_ATMOSFERICA + rules.RANGO_PRES_ATM:
                logger.warning("No se puede cerrar la puerta: presión de empaque alta.")
                return False
        
        return True

    #=============================
    #PARTICION DE ACTUALIZACION
    #=============================
    def update(self):
        # -No mueve nada
        # -No enciende/apaga nada
        # -No decide transiciones de estado
        # -Observar el estado actual
        # -Detecta cambio de estado
        # -Reacciona a estados criticos
        # -Registra / Notifica
        
        for door in self.doors:
            current_state = door.state
            last_state = self._last_states[door]
            
            # Primera ejecución
            if last_state is None:
                self._last_states[door] = current_state
                continue
        
            # Ningún cambio de estado
            if current_state == last_state:
                continue
            
            # Cambio de estado detectado
            self._on_state_change(door, last_state, current_state)
            #Actualizamos el estado anterior
            self._last_states[door] = current_state
        
        
    def _on_state_change(self, door, prev, current):
        
        if self.logger:
            self.logger.info(
                f"Puerta {door.name}: {prev.name} -> {current.name}"
                )
        
        if current == DoorState.ERROR:
            self._handle_error(door)
            
        elif current == DoorState.ABRIENDO:
            self._handle_opening(door)
        
        elif current == DoorState.ABIERTO:
            self._handle_opened(door)
            
        
        elif current == DoorState.CERRANDO:
            self._handle_closing(door)
        
        elif current == DoorState.CERRADO:
            self._handle_closed(door)
            
        elif current == DoorState.ATRAPADA:
            self._handle_jammed(door)   
        

    def _handle_error(self, door):
        if self.logger:
            self.logger.error(f"¡Error en puerta {door.name}!")
            
    def _handle_opening(self, door):
        if self.logger:
            self.logger.info(f"Puerta {door.name} abriéndose...")
            
    def _handle_opened(self, door):
        if self.logger:
            self.logger.info(f"Puerta {door.name} abierta.")
            
    def _handle_closing(self, door):
        if self.logger:
            self.logger.info(f"Puerta {door.name} cerrándose...")
            
    def _handle_closed(self, door):
        if self.logger:
            self.logger.info(f"Puerta {door.name} cerrada.")
    
    def _handle_jammed(self, door):
        if self.logger:
            self.logger.error(f"¡Puerta {door.name} atrapada!")
            


    #=============================
    #UTILIDADES INTERNAS
    #=============================
    
    def log (self, message):
        if self.logger:
            self.logger.info(message)
    
    def event (self, event_type, message):
        if self.logger:
            self.logger.info(f"[{event_type}] {message}")
            
    def error (self, message):
        if self.logger:
            self.logger.error(message)
            
