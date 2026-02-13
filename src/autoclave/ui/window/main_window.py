# autoclave/ui/main_window.py

#Importar librerias necesarias
import PIL.Image as image
import tkinter as tk
import customtkinter as ctk
import logging
import autoclave.ui.components as components
from autoclave.ui.cycle.cycle_window import CycleWindow
from autoclave.utils.resources import resource_path


#configuracion del logger
logger = logging.getLogger(__name__)
#variables globales de la interfaz

titulo_ciclo_texto = "Bowie and Dick"

#----------------------------------------------------------------------
class InterfazPrincipal(tk.Tk):

    #inicializacion de la interfaz principal
    def __init__(self, ui_service, door_commands):
        super().__init__()
        # Configuración de la ventana principal, tamaño y color de fondo, abre en pantalla completa
        self.title("Autoclave de vapor")
        self.geometry("1280x720")
        self.configure(bg="#b6ccd9")
        self.attributes("-fullscreen", True)
        
    
        #variables globales de la interfaz
        self.ui_service = ui_service
        self.prep_ciclo= self.ui_service.get_estado_global()
        self.alarmas_activas = self.ui_service.get_alarmas()
        self.n_ciclo= tk.IntVar(value=1)
        self.door_commands = door_commands

        
        #inicia las partes de la interfaz
        components._crear_encabezado(self, "T-MAX6")
        self.crear_layout()
        self._pie_pagina()
        logger.info("✅ Interfaz creada correctamente.")

    # ------------------------------------------------------------------
    # Creación de la interfaz
    # ------------------------------------------------------------------
    
    #creacion del encabezado: este codigo crea el encabezado de la interfaz principal
    #estara en la parte superior de la ventana ocupara todo el ancho de la ventana y tendra un 6.6% de alto, con un color de fondo #5789a7


    def crear_layout(self):
        #este codigo creara un contenedor con las esquinas redondeadas, color blanco #ffffff mediante la libreria customtkinter que estara en la parte central de la ventana
        #separada del encavezado por un espacio de 10 pixeles y separada de los bordes laterales por un espacio correspondiente al 4% del ancho de la ventana
        #y una altura correspondiente al 75.25% de la altura de la ventana
        fondo = components._crear_fondo_principal (self)

        def contenedor_estados(fondo):
            #este codigo creara un contenedor dentro del contenedor fondo, con las esquinas redondeadas en un radio de 30px y color celeste oscuro apagado #2d4757 mediante la libreria customtkinter,
            #este iniciara al lado izquierdo de la ventana principal, separado del borde izquierdo por un espacio correspondiente al 4.5% del ancho de la ventana 
            # y del borde superior por un espacio correspondiente al 5% de la altura de la ventana,
            #tendra un ancho correspondiente al 22.5% del ancho de la ventana y una altura correspondiente al 64% de la altura de la ventana
            estados = ctk.CTkFrame(
                fondo,
                corner_radius=40,
                bg_color="#ffffff",
                fg_color="#2d4757",
            )
            estados.place(
                relx=0.03,
                rely=0.06,
                relwidth=0.245,
                relheight=0.88,
            )
            
            def numero_ciclo(cont):
                #este codigo creara un label dentro del contenedor estados, que mostrara el numero de ciclo actual
                #el label estara en la parte superior del contenedor estados, centrado, separado del borde superior por un espacio correspondiente al 10% de la altura del contenedor estados
                #este numero tendra un tamaño equivalente al 50% del ancho del contenedor estados
                #el label tendra un color de fondo #2d4757 y un color de letra blanco, con una fuente Segoe UI de tamaño 24 y negrita
                ciclo_label = ctk.CTkLabel(
                    cont,
                    text=self.n_ciclo.get(),
                    font=("Segoe UI", 80, "bold"),
                    bg_color="#2d4757",
                    fg_color="#2d4757",
                    text_color="white",
                )
                ciclo_label.place(
                    relx=0.5,
                    rely=0.05,
                    anchor="n",
                )
            numero_ciclo(estados)
            
            def estado_actual(cont):
                #este codigo creara un label dentro del contenedor estados, que mostrara el estado actual del sistema
                #almacenado en la variable prep_ciclo de tipo StringVar
                #el label estara debajo del label del numero de ciclo, alineado a la hisquierda del contenedor estados, separado del borde izquierdo por un espacio correspondiente al 5% del ancho del contenedor estados
                #y separado del label del numero de ciclo por un espacio correspondiente al 5% de la altura del contenedor estados
                
                estado_label = ctk.CTkLabel(
                    cont,
                    text= self.prep_ciclo,
                    font=("Segoe UI", 20, "bold"),
                    bg_color="#2d4757",
                    fg_color="#2d4757",
                    text_color="white",
                    
                )
                estado_label.place(
                    relx=0.05,
                    rely=0.3,
                    anchor="w",
                )
                cont.after(5000, estado_actual, cont)  # actualizar cada 5 segundos
            estado_actual(estados)
            
            def info_alarmas (cont):
                #este codigo  creara labels uno bajo el otro dentro del contenedor estados, que mostraran la informacion de las alarmas activas
                #estas alarmas estaran almacenadas en una lista de strings llamada alarmas_activas
                #este se actualizara cada 5 segundos para mostrar las alarmas activas actuales
                #si la lista esta vacia, no se mostrara nada
                #el primer label estara debajo del label del estado actual, alineado a la izquierda del contenedor estados, separado del borde izquierdo por un espacio correspondiente al 5% del ancho del contenedor estados
                #y separado del label del estado actual por un espacio correspondiente al 5% de la altura del contenedor estados
                    #eliminar labels anteriores
                self.alarmas_activas = self.ui_service.get_alarmas()
                #print("ui_main Alarmas activas:", self.alarmas_activas)
                for widget in cont.winfo_children():
                    if isinstance(widget, ctk.CTkLabel) and widget != cont.winfo_children()[0] and widget != cont.winfo_children()[1]:
                        widget.destroy()
                #crear nuevos labels
                for i, alarma in enumerate(self.alarmas_activas):
                    alarma_label = ctk.CTkLabel(
                        cont,
                        text= f"[{alarma['level']}] {alarma['id']}",
                        font=("Segoe UI", 16),
                        bg_color="#2d4757",
                        fg_color="#2d4757",
                        text_color="white",
                    )
                    alarma_label.place(
                        relx=0.05,
                        rely=0.4 + i*0.05,
                        anchor="w",
                    )
                #llamar a esta funcion cada 5 segundos para actualizar las alarmas
                cont.after(5000, info_alarmas, cont)
            info_alarmas(estados)
        contenedor_estados(fondo)

        def titulo_ciclo(fondo):
            #este codigo creara un label dentro del contenedor fondo, que mostrara el titulo "Ciclo de esterilizacion"
            #este label estara en la parte superior central del contenedor fondo, separado del borde superior por un espacio correspondiente al 9% de la altura del contenedor fondo
            #tendra un ancho correspondiente al 40% del ancho del contenedor fondo
            texto= titulo_ciclo_texto.upper()
            titulo_label = ctk.CTkLabel(
                fondo,
                text= texto,
                font=("Segoe UI", 60, "bold"),
                bg_color="#ffffff",
                fg_color="#ffffff",
                text_color="Black",
            )
            titulo_label.place(
                relx=0.635,
                rely=0.09,
                anchor="n",
            )
        titulo_ciclo(fondo)
    
        def linea_separadora(fondo):
            #este codigo creara una linea separadora horizontal dentro del contenedor fondo
            #esta linea estara en la parte superior del contenedor fondo, separada del borde superior por un espacio correspondiente al 18% de la altura del contenedor fondo
            #tendra un ancho correspondiente al 92% del ancho del contenedor fondo y una altura de 2 pixeles
            linea = ctk.CTkFrame(
                fondo,
                bg_color="#ffffff",
                fg_color="black",
            )
            linea.place(
                relx=0.64,
                rely=0.24,
                anchor="n",
                relwidth=0.6,
                relheight=0.008,
            )
        linea_separadora(fondo)

        #este fragmento de codigo creara 3 contenedores dentro del contenedor fondo llamando a la funcion _crear_contenedor_informacion desde el modulo components
        #estos contenedores estaran dispuests de forma vertical en la parte dereca del contenedor fondo a una distancia del borde hisquierdo correspondoente al 32.4% del ancho del contenedor fondo
        #el primer contenedor estara separado del borde superior del contenedor fondo por un espacio correspondiente al 26% de la altura del contenedor fondo
        #una separacion entre cada contenedor correspondiente al 5% de la altura del contenedor fondo
        def parm_temp(fondo):
            contenedor1 = components._crear_contenedor_informacion(
                fondo,
                relx=0.324,
                rely=0.26,
                relwidth=0.294,
                relheight=0.105,
            )
            def info_par_temp(cont):
                components._info_contenedor(
                cont,
                "Temp.Ester",
                "134",
                "°C"
            )
            info_par_temp(contenedor1)
        parm_temp(fondo)

        def parm_tiempo(fondo):
            contenedor2 = components._crear_contenedor_informacion(
                fondo,
                relx=0.324,
                rely=0.26 + 0.105 + 0.05,
                relwidth=0.294,
                relheight=0.105,
        )
            def info_par_tiempo(cont):
                components._info_contenedor(
                cont,
                "Tiempo.Ester",
                "5",
                "min"
            )
            info_par_tiempo(contenedor2)
        parm_tiempo(fondo)
        
        def parm_secado(fondo):
            contenedor3 = components._crear_contenedor_informacion(
            fondo,
            relx=0.324,
            rely=0.26 + 0.105 + 0.05 + 0.105 + 0.05,
            relwidth=0.294,
            relheight=0.105,
        )
            def info_par_secado(cont):
                components._info_contenedor(
                cont,
                "Tiempo.Secado",
                "2",
                "min"
            ) 
            info_par_secado(contenedor3)
        parm_secado(fondo)

        #este fragmento de codigo creara 3 contenedores dentro del contenedor fondo llamando a la funcion _crear_contenedor_informacion desde el modulo components
        #estos contenedores estaran dispuests de forma vertical en la parte derecha del contenedor fondo a una distancia del borde izquierdo correspondoente al 65.8% del ancho del contenedor fondo
        #el primer contenedor estara separado del borde superior del contenedor fondo por un espacio correspondiente al 26% de la altura del contenedor fondo
        #una separacion entre cada contenedor correspondiente al 5% de la altura del contenedor fondo
        def inf_t_cam(fondo):
            #actualizaciond el contenedor:
            #el valor de la temperatura de la camara actualizara por medio del control loop
            #por lo cual leera un estado actual llamado temp_camara
            self.contenedor_t_cam = components._crear_contenedor_informacion(
                fondo,
                relx=0.658,
                rely=0.26,
                relwidth=0.294,
                relheight=0.105,
            )
            label = components._info_sensors(
                self.contenedor_t_cam,
                "Temp.Cam",
                "°C",
            )
            #valor label en el centro
            self.temp_cam = ctk.CTkLabel(
                self.contenedor_t_cam,
                text="---",
                font=("Segoe UI", 20, "bold"),
                bg_color="#2d4757",
                fg_color="#2d4757",
                text_color="white",
            )
            self.temp_cam.pack(side=tk.RIGHT, padx=10)
            
            
        inf_t_cam(fondo)
        
        def inf_t_ref(fondo):
            self.contenedor_t_ref = components._crear_contenedor_informacion(
                fondo,
                relx=0.658,
                rely=0.26 + 0.105 + 0.05,
                relwidth=0.294,
                relheight=0.105,
            )

            label = components._info_sensors(
                self.contenedor_t_ref,
                "Temp.Ref",
                "°C",
            )
            #valor label en el centro
            self.temp_ref = ctk.CTkLabel(
                self.contenedor_t_ref,
                text="---",
                font=("Segoe UI", 20, "bold"),
                bg_color="#2d4757",
                fg_color="#2d4757",
                text_color="white",
            )
            self.temp_ref.pack(side=tk.RIGHT, padx=10)
        
        inf_t_ref(fondo)
        
        def inf_pres_cam(fondo):
            contenedor6 = components._crear_contenedor_informacion(
                fondo,
                relx=0.658,
                rely=0.26 + 0.105 + 0.05 + 0.105 + 0.05,
                relwidth=0.294,
                relheight=0.105,
            )
            label = components._info_sensors(
                contenedor6,
                "Pres.Cam",
                "kPa",
            )
            #valor label
            self.pres_cam = ctk.CTkLabel(
                contenedor6,
                text="---",
                font=("Segoe UI", 20, "bold"),
                bg_color="#2d4757",
                fg_color="#2d4757",
                text_color="white",
            )
            self.pres_cam.pack(side=tk.RIGHT, padx=10)

        inf_pres_cam(fondo)
        self.actualizar_sensores()

#-----------------------------------------------------------------------
    #botones inferiores para control de la puerta y ciclo
#-----------------------------------------------------------------------
        def boton_puerta_1(fondo, door_commands):
            #creacion del boton para abrir y cerrar la puerta
            #este boton estara en la parte inferior izquierda del contenedor fondo, separado del borde izquierdo por un espacio correspondiente al 4.5% del ancho del contenedor fondo
            #y separado del borde inferior por un espacio correspondiente al 5% de la altura del contenedor fondo
            #tendra una n de puerta hubicada en src/autoclave/images/open_door.png
                
            def accion_boton():
                estado_actual = self.ui_service.get_estado_puerta("Puerta 1")
                
                if estado_actual == "ABIERTO":
                    door_commands.close("Puerta 1")
                else:
                    door_commands.open("Puerta 1")
                    
                actualizar_boton()
            #creacion del boton
            boton_puerta = ctk.CTkButton(
                fondo,
                text="",
                compound="left",
                fg_color="white",
                hover_color="lightgray",
                command=accion_boton
            )
            
            boton_puerta.place(
                relx=0.324,
                rely=0.73,
                relwidth=0.06,
                relheight=0.18,
            )
            
        

        
        
            def actualizar_boton():
                estado_actual = self.ui_service.get_estado_puerta("Puerta 1")
                
                if estado_actual == "CERRADO":
                    img= ctk.CTkImage(
                        light_image=image.open(
                            resource_path("autoclave/images/close_door_1.png")),
                        dark_image=image.open(resource_path("autoclave/images/close_door_1.png")),
                        size=(200, 100),
                    )
                    
                else:
                    img= ctk.CTkImage(
                        light_image=image.open(resource_path("autoclave/images/open_door_1.png")),
                        dark_image=image.open(resource_path("autoclave/images/open_door_1.png")),
                        size=(200, 100),
                    )
                
                boton_puerta.configure(image=img)
                boton_puerta.image = img  # Mantener una referencia a la imagen

            def actualizar_boton_periodico():
                actualizar_boton()
                fondo.after(200, actualizar_boton_periodico)  # cada 200 ms

            actualizar_boton_periodico()
        boton_puerta_1(fondo, self.door_commands)

        def boton_puerta_2(fondo, door_commands, door_index="Puerta 2"):
            #esto mostrara el estado de la segunda puerta
            #este estara en la parte inferior central del contenedor fondo, separado del borde izquierdo por un espacio correspondiente al 47.5% del ancho del contenedor fondo
            #y separado del borde inferior por un espacio correspondiente al 5% de la altura del contenedor fondo
            #tendra una imagen de puerta hubicada en src/autoclave/images/
            
            def accion_boton_2():
                estado_actual = self.ui_service.get_estado_puerta(door_index)
                
                if estado_actual == "ABIERTO":
                    door_commands.close(door_index)
                else:
                    door_commands.open(door_index)
                    
                actualizar_puerta_dos()
            
            boton_puerta_dos = ctk.CTkButton(
                fondo,
                text="",
                compound="left",
                fg_color="white",
                hover_color="lightgray",
                command=accion_boton_2
            )
            boton_puerta_dos.place(
                relx=0.384,
                rely=0.728,
                relwidth=0.06,
                relheight=0.18,
            )
            
            def actualizar_puerta_dos():
                estado_puerta_2 = self.ui_service.get_estado_puerta(door_index)
                
                if estado_puerta_2 == "CERRADO":
                    img= ctk.CTkImage(
                        light_image=image.open(
                            resource_path("autoclave/images/close_door_2.png")),
                        dark_image=image.open(resource_path("autoclave/images/close_door_2.png")),
                        size=(200, 100),
                    )
                else:
                    img= ctk.CTkImage(
                        light_image=image.open(resource_path("autoclave/images/open_door_2.png")),
                        dark_image=image.open(resource_path("autoclave/images/open_door_2.png")),
                        size=(200, 100),
                    )
                boton_puerta_dos.configure(image=img)
                boton_puerta_dos.image = img  # Mantener una referencia a la imagen
                
            def actualizar_puerta_dos_periodico():
                actualizar_puerta_dos()
                fondo.after(200, actualizar_puerta_dos_periodico)  # cada 200 ms
            actualizar_puerta_dos_periodico()
        boton_puerta_2(fondo, self.door_commands, door_index="Puerta 2")


        def boton_iniciar_ciclo():
            #creacion del boton para iniciar el ciclo
            #este boton estara en la parte inferior derecha del contenedor fondo, separado del borde derecho por un espacio correspondiente al 4.5% del ancho del contenedor fondo
            #y separado del borde inferior por un espacio correspondiente al 5% de la altura del contenedor fondo
            #tendra una imagen de inicio hubicada en src/autoclave/images/start_cycle.png
            img= ctk.CTkImage(
                light_image=image.open(resource_path("autoclave/images/start_cycle.png")),
                dark_image=image.open(resource_path("autoclave/images/start_cycle.png")),
                size=(200, 100),
            )
            #el boton al ser presionado llamara a la funcion start_cycle
            boton_iniciar = ctk.CTkButton(
                fondo,
                text="",
                image=img,
                compound="left",
                #banco
                fg_color="white",
                #gris claro
                hover_color="lightgray",
                command=self.start_cycle
            )
            boton_iniciar.place(
                relx=0.85,
                rely=0.73,
                relwidth=0.1,
                relheight=0.18,
            )
        boton_iniciar_ciclo()

    def _pie_pagina(self):
        #el pie de pagina estara en la parte inferior de la ventana principal, centrado con un ancho correnpondiante al 55% del ancho de la ventana, con esquinas redondeadas de 40px
        #y una altura correspondiente al 12% de la altura de la ventana, con un color de fondo #5789a7
        pie_pagina = components._crear_pie_pagina(self)
        
        
        def boton_info(pie_pagina):
            #creacion del boton informacion
            #este bototon estara en la parte izquierda del pie de pagina, separado del borde izquierdo por un espacio correspondiente al 5% del ancho del pie de pagina
            #y centrado verticalmente en el pie de pagina
            img= ctk.CTkImage(
                light_image=image.open(resource_path("autoclave/images/info_icon.png")),
                dark_image=image.open(resource_path("autoclave/images/info_icon.png")),
                size=(80, 40),
            )
            boton_info = ctk.CTkButton(
                pie_pagina,
                corner_radius=100,
                text="",
                image=img,
                compound="left",
                fg_color="#5789a7",
                hover_color="#406080",
            )
            boton_info.place(
                relx=0.05,
                rely=0.5,
                anchor="w",
                relwidth=0.1,
                relheight=0.7,
            )
        boton_info(pie_pagina)
        def boton_login(pie_pagina):
            #creacion del boton login
            #este bototon estara en la parte derecha del pie de pagina, separado del borde derecho por un espacio correspondiente al 5% del ancho del pie de pagina
            #y centrado verticalmente en el pie de pagina
            img= ctk.CTkImage(
                light_image=image.open(
                    resource_path("autoclave/images/login_icon.png")),
                dark_image=image.open(resource_path("autoclave/images/login_icon.png")),
                size=(100, 50),
            )
            boton_login = ctk.CTkButton(
                pie_pagina,
                corner_radius=50,
                text="",
                image=img,
                compound="left", 
                fg_color="#5789a7",
                hover_color="#406080",
                command=self.login_user,
            )
            boton_login.place(
                relx=0.95,
                rely=0.5,
                anchor="e",
                relwidth=0.1,
                relheight=0.7,
            )
        boton_login(pie_pagina)
        
        def boton_apagar(pie_pagina):
            #creacion del boton apagar
            #este bototon estara en el centro del pie de pagina, centrado verticalmente en el pie de pagina
            img= ctk.CTkImage(
                light_image=image.open(resource_path("autoclave/images/power_icon.png")),
                dark_image=image.open(resource_path("autoclave/images/power_icon.png")),
                size=(80, 40),
            )
            boton_apagar = ctk.CTkButton(
                pie_pagina,
                corner_radius=100,
                text="",
                image=img,
                compound="left",
                fg_color="#5789a7",
                hover_color="#406080",
                command=self.apagar_equipo,
            )
            boton_apagar.place(
                relx=0.5,
                rely=0.5,
                anchor="c",
                relwidth=0.1,
                relheight=0.7,
            )
        boton_apagar(pie_pagina)

    def start_cycle(self):
        #funcion para iniciar el ciclo de esterilizacion
        #esta funcion abrira una nueva ventana llamando a la clase CycleWindow del modulo cycle_window
        logger.info("▶️ Iniciando ciclo de esterilización...")
        cycle_window = CycleWindow(self)
        cycle_window.grab_set()

    def apagar_equipo(self):
        #funcion para apagar el equipo
        logger.info("⏻ Apagando equipo...")
        #la pantalla se oscurecera y aparecera un mensaje de apagando equipo, luego de 3 segundos la aplicacion se cerrara
        self.withdraw()
        apagando_ventana = tk.Toplevel(self)
        apagando_ventana.geometry("400x200")
        apagando_ventana.title("Apagando equipo")
        apagando_ventana.configure(bg="#37596C")
        #transparencia
        apagando_ventana.wm_attributes("-alpha", 0.9)
        apagando_ventana.attributes("-fullscreen", True)
        mensaje = ctk.CTkLabel(
            apagando_ventana,
            text="Apagando equipo...",
            font=("Segoe UI", 40, "bold"),
            bg_color="#37596C",
            fg_color="#37596C",
            text_color="white",
        )
        mensaje.pack(expand=True)
        apagando_ventana.after(3000, self.destroy)

    def login_user(self):
        #funcion para login de usuario
        pass  # Implementar funcionalidad de login aquí

    def actualizar_sensores(self,):
        #funcion para actualizar el valor de la temperatura de la camara
        valor_temp = self.ui_service.get_sensores_temp()
        valor_pres = self.ui_service.get_sensores_pres()
        self.temp_cam.configure(text=str(valor_temp["temp_camara"]))
        self.temp_ref.configure(text=str(valor_temp["temp_ref"]))
        
        self.pres_cam.configure(text=str(valor_pres["pres_camara"]))
        self.after(500, self.actualizar_sensores)
        
        #llama a esta funcion cada 500ms para actualizar el valor
    
    def toggle_door(self):
        door=self.door_commands.doors[0]
        status=door.state.name
        
        if status == "ABIERTO":
            self.door_commands.request_close(door)
            
        else:
            self.door_commands.request_open(door)