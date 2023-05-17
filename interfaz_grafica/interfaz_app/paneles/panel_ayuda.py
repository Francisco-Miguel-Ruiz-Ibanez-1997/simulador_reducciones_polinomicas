import tkinter as tk
import customtkinter as ctk

from PIL import Image

from .panel import Panel

#####################################################
# Clase que contiene el panel de ayuda del simulador
# con el que el usuario puede obtener información 
# sobre su uso y manejo.
#####################################################
class PanelAyuda(Panel):

    # Constructor.
    def __init__(self, ventana=None):

        # Constructor del padre
        super().__init__(ventana)
        self.pack()
        self.mostrar_ayuda()
    
    # Función que muestra información sobre uso y manejo de la 
    # aplicación.
    def mostrar_ayuda(self):

        panel_ayuda = ctk.CTkFrame(self, fg_color=("#6889B1","gray20"))
        panel_ayuda.pack(fill='both', pady=20, padx=20, side='left', expand=True)

        panel_tabview = ctk.CTkTabview(panel_ayuda, fg_color=("#1D1E78","gray27"))
        panel_tabview.pack(side="top", padx=20, pady=20, fill="both", expand=True)

        # Pestañas del panel ayuda
        panel_tabview.add("¿Qué hace la aplicación?")
        panel_tabview.add("Controles y botones principales")
        panel_tabview.add("Poli-reducciones")
        panel_tabview.add("Info sobre problemas")
        panel_tabview.add("Solver para SAT3cnf")
        panel_tabview.add("Cook-Levin")

        ########################## Descripción general
        texto = "El simulador de reducciones polinómicas es una aplicación en la que el usuario puede seleccionar dos problemas y realizar\n" \
            "la poli-reducción entre ellos, simulando, por tanto, la realización de tal reducción. Proporciona así una herramienta \n" \
            "didáctica en la que el usuario puede ir visualizando cómo se realiza la poli-reducción escogida, mostrándose siempre los \n" \
            "pasos que se desarrollan y exponiendo las conclusiones finales, como por ejemplo, si A se poli-reduce a B y A es NP-Completo y \n" \
            "B es NP, entonces B será NP-Completo. Por tanto, también demuestra la NP-Completitud de problemas en caso de que se \n" \
            "se produzca.\n\n\n" \
            "Además de la simulación de las reducciones, el usuario podrá obtener información sobre los problemas que podrá\n" \
            "poli-reducir, pudiendo así ver en qué consisten.\n\n\n" \
            "A todas estas funcionalidades anteriores se añade la del solver para fórmulas en forma 3-cnf, de forma que la aplicación\n" \
            "también podrá dar solución a fórmulas en forma 3-cnf introducidas por el usuario, informando a este de su satisfacibilidad.\n" \
            "A todo esto hay que añadir la reducción Cook-Levin que se puede simular."

        panel = ctk.CTkFrame(panel_tabview.tab("¿Qué hace la aplicación?"))
        panel.pack(side="top", fill="both", expand=True)

        label = ctk.CTkLabel(panel, text=texto)
        label.pack(side="top", padx=10, pady=10)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info_general_app.png"), size=(500, 370))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="bottom",padx=10, pady=10)

        ########################## Controles principales
        panel = ctk.CTkFrame(panel_tabview.tab("Controles y botones principales"))
        panel.pack(side="top", fill="both", expand=True)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/controles_principales.png"), size=(600, 400))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="top",padx=10, pady=10, fill="both")

        panel_1 = ctk.CTkFrame(panel)
        panel_1.pack(side="left", fill="both", expand=True)

        lista_texto = []

        texto = "Botón [Inicio]. Regresa al panel principal (la imagen que se muestra arriba) de la aplicación, que permite realizar la simulación de las poli-reducciones."

        lista_texto.append(texto)

        texto = "Botón [Repertorio de problemas]. Muestra el panel de repertorio de problemas (lenguajes) de la aplicación, que contiene información sobre ellos."
        lista_texto.append(texto)

        texto = "Botón [Ayuda]. Cambia al panel de ayuda de la aplicación, que contiene información sobre su uso y manejo."
        lista_texto.append(texto)

        texto = "Modo/tema de la aplicación. A escoger temas claro y oscuro."
        lista_texto.append(texto)

        texto = "Botón [Más]. Abre una ventana con un menú para lanzar el solver DPLL para fórmulas en forma 3-cnf o la reducción Cook-Levin."
        lista_texto.append(texto)

        texto = "Botón [Salir]. Sale de la aplicación."
        lista_texto.append(texto)

        texto = "Combo-box para selección del primer problema."
        lista_texto.append(texto)

        texto = "Combo-box para selección del segundo problema."
        lista_texto.append(texto)

        texto = "Botón [Repintar universo]. Vuelve a pintar el universo de problemas y sus relaciones."
        lista_texto.append(texto)

        texto = "Botón [Resetear poli-reducciones]. Resetea las poli-reducciones (si ya estaban realizadas, ahora se podrán volver a realizar) y actualiza el universo."
        lista_texto.append(texto)

        texto = "Botón [Iniciar simulador]. Inicia la poli-reducción entre los problemas seleccionados."
        lista_texto.append(texto)

        letras = ["A","B","C","D","E","F","G","H","I","J","K"]
        texto_inicial = ""
        lista_texto_final = []

        self.crear_leyenda_info(panel_1, letras, lista_texto, texto_inicial, lista_texto_final)

        ########################## Poli-reducciones
        panel = ctk.CTkFrame(panel_tabview.tab("Poli-reducciones"))
        panel.pack(side="top", fill="both", expand=True)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/seleccion_problemas.png"), size=(600, 400))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="top",padx=10, pady=10, fill="both")

        panel_1 = ctk.CTkFrame(panel)
        panel_1.pack(side="left", fill="both", expand=True)

        lista_texto = []

        texto = "Escogemos el problema que queremos reducir."

        lista_texto.append(texto)

        texto = "Escogemos el problema al que vamos a reducir."
        lista_texto.append(texto)

        texto = "Iniciamos la simulación al pulsar [Iniciar simulador]. Se abrirá una ventana informando sobre lo que se va a realizar (en caso de que exista poli-reducción)."
        lista_texto.append(texto)

        texto = "Para iniciar la poli-reducción, pulsaremos [Aceptar]."
        lista_texto.append(texto)

        orden = ["1º","2º","3º", "4º"]
        texto_inicial = "Para comenzar la poli-reducción entre problemas, estando en el panel 'Inicio', realizaremos los siguientes pasos:"
        lista_texto_final = ["NOTA: Al pulsar sobre [Iniciar simulador], si no existe poli-reducción entre los problemas seleccionados, o falta alguno de ellos por introducir, se informará de ello."]

        self.crear_leyenda_info(panel_1, orden, lista_texto, texto_inicial, lista_texto_final)

        ########################## Info sobre repertorio
        panel = ctk.CTkFrame(panel_tabview.tab("Info sobre problemas"))
        panel.pack(side="top", fill="both", expand=True)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/info_repertorio.png"), size=(600, 400))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="top",padx=10, pady=10, fill="both")

        panel_1 = ctk.CTkFrame(panel)
        panel_1.pack(side="left", fill="both", expand=True)

        lista_texto = ["Escogemos el problema sobre el que queremos ver información."]
        orden = ["1º"]
        texto_inicial = "Para visualizar información sobre los problemas, estando en el panel 'Repertorio de problemas', haremos:"
        lista_texto_final = ["Al seleccionar un problema sobre el que ver información, se mostrará información sobre este y se visualizará un código QR que redirige a una web con más detalles sobre el problema."]

        self.crear_leyenda_info(panel_1, orden, lista_texto, texto_inicial, lista_texto_final)

        ########################## Solver SAT3cnf
        panel = ctk.CTkFrame(panel_tabview.tab("Solver para SAT3cnf"))
        panel.pack(side="top", fill="both", expand=True)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/controles_solver.png"), size=(600, 400))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="top",padx=10, pady=10, fill="both")

        panel_1 = ctk.CTkFrame(panel)
        panel_1.pack(side="left", fill="both", expand=True)

        lista_texto = []

        texto = "Introducimos una fórmula en forma 3-cnf."
        lista_texto.append(texto)

        texto = "Una vez introducimos una fórmula, pulsamos el botón [Introducir]."
        lista_texto.append(texto)

        texto = "Si la fórmula es correcta y está en formato 3-cnf, entonces al pulsar [Resolver fórmula] nos resolverá la fórmula introducida, mostrando si es satisfacible (con los valores que la satisfacen) o si no lo es."
        lista_texto.append(texto)

        texto = "Si el usuario duda qué formato tiene una fórmula en forma 3-cnf, pulsará el botón [Más info], que muestra qué formato debe utilizar."
        lista_texto.append(texto)

        texto = "En caso de borrar la fórmula introducida, puede pulsar el botón [Limpiar] o bien borrarla manualmente en la entrada de texto que se muestra en el 1º paso."
        lista_texto.append(texto)

        orden = ["1º","2º","3º", "*", "**"]
        texto_inicial = "Para resolver una fórmula en formato 3-cnf, realizaremos los siguientes pasos:"
        lista_texto_final = ["Al introducir una fórmula correcta, se mostrará información relativa a esta.", 
                                "NOTA: Si el usuario introduce una fórmula incorrecta, se informará de los errores cometidos, así como de los errores sintácticos como léxicos."]

        self.crear_leyenda_info(panel_1, orden, lista_texto, texto_inicial, lista_texto_final)

        ########################## Reducción Cook-Levin
        panel = ctk.CTkFrame(panel_tabview.tab("Cook-Levin"))
        panel.pack(side="top", fill="both", expand=True)

        bg_image = ctk.CTkImage(Image.open("interfaz_grafica/interfaz_app/img/controles_cook_levin.png"), size=(560, 450))
        bg_image_label = ctk.CTkLabel(panel, text="", image=bg_image)
        bg_image_label.pack(side="top",padx=10, pady=10, fill="both")

        panel_1 = ctk.CTkFrame(panel)
        panel_1.pack(side="left", fill="both", expand=True)

        lista_texto = []

        texto = "Seleccionamos una MT (en formato .jff o .txt)."
        lista_texto.append(texto)

        texto = "Introducimos una palabra que acepta la MT, escribiéndola en el cuadro de texto y pulsando [Introducir]."
        lista_texto.append(texto)

        texto = "Si se han introducido ambos campos anteriores, entonces al pulsar [Lanzar reducción] nos lanzará la simulación Cook-Levin en la terminal."
        lista_texto.append(texto)

        orden = ["1º","2º","3º"]
        texto_inicial = "Para lanzar la simulación Cook-Levin realizaremos los siguientes pasos:"
        lista_texto_final = ["NOTA: Cerrar la simulación introduciendo el comando [q] antes de cerrar la aplicación principal."]

        self.crear_leyenda_info(panel_1, orden, lista_texto, texto_inicial, lista_texto_final)
    
    # Crea el panel leyenda con la información detallada de los pasos o controles que 
    # hay que seguir.
    def crear_leyenda_info(self, panel, nombre_labels, lista_texto, texto_inicial, lista_texto_final):

        pos = 0

        canvas = tk.Canvas(panel, width=170, height=170)
        scrolly = tk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollx = tk.Scrollbar(panel, orient="horizontal", command=canvas.xview)

        i = 0

        # Separación label-canvas. Texto inicial sobre lo que se va a realizar
        label = tk.Label(canvas, text=texto_inicial)
        canvas.create_window(0, 20, anchor='nw', window=label)
        i +=1

        # Leyenda botones y pasos a seguir
        for texto in lista_texto:

            label = tk.Label(canvas, borderwidth=1, text=nombre_labels[pos], font=tk.font.Font(size=10, weight="bold"), fg="red", background="yellow")
            canvas.create_window(10, i*50, anchor='nw', window=label, width=25, height=25)

            label = tk.Label(canvas, text=" " + texto)
            canvas.create_window(45, i*50, anchor='nw', window=label)
            
            i += 1
            pos += 1

        # Texto final sobre lo que se va a realizar. Contiene texto extra al anterior
        # o anotaciones
        for texto_final in lista_texto_final:

            label = tk.Label(canvas, text=texto_final)
            canvas.create_window(0, i*50, anchor='nw', window=label)

            i += 0.5

        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scrolly.set)
        canvas.configure(scrollregion=canvas.bbox('all'), xscrollcommand=scrollx.set)

        scrollx.pack(side="bottom", fill=tk.X)
        scrolly.pack(side="right", fill=tk.Y)
        canvas.pack(padx=50, pady=10,side="bottom", fill="both", expand=True)
