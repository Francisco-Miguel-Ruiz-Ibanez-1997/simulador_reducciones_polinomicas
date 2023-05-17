import tkinter as tk
import customtkinter as ctk

from .etapa import Etapa

################################################################
# Clase que engloba la última etapa a realizar.  
# Tras la poli-reducción realizada, ahora terminaremos probando
# que HAMCYCLE es NP-Completo. Esto se debe a la aplicación del 
# Tercer Teorema de la Reducibilidad.
################################################################
class Etapa2(Etapa):

    def __init__(self, ventana, gestor_etapas):

        super().__init__(ventana, gestor_etapas)
    
     ### Getters y setters ###

    def get_panel_2(self):
        return self.panel_2

    ### Lanzador de etapa ###
    
    def lanzar_etapa(self):
        # Realizamos etapa
        self.etapa_realizada = True

        # Creamos nuevo panel
        self.panel_2 = ctk.CTkFrame(self.ventana, corner_radius=0)
        self.panel_2.pack(padx=10, pady=10, fill="both",expand=True)

        panel_titulo = ctk.CTkFrame(self.panel_2, fg_color="#6889B1")
        panel_titulo.pack(padx=30, pady=30, fill=tk.X)

        label = ctk.CTkLabel(panel_titulo, text = "3º: Tercer Teorema de la Reducibilidad", fg_color="#6889B1",
                                font=ctk.CTkFont(size=20, weight="bold"))
        label.pack(padx=10, pady=10)

        panel_subtitulo = ctk.CTkFrame(self.panel_2, fg_color="#A4B6CD")
        panel_subtitulo.pack(padx=30, pady=(50,10))

        label = ctk.CTkLabel(panel_subtitulo, text="HAMCYCLE es NP-Completo", fg_color="#A4B6CD",
                                font=ctk.CTkFont(size=14,weight="bold"))
        label.pack(padx=30, pady=10)

        panel_texto = ctk.CTkFrame(self.panel_2)
        panel_texto.pack(padx=10,pady= 10)

        label = ctk.CTkLabel(panel_texto, text="Por último, aplicaremos el tercer teorema de la reducibilidad:")
        label.pack(padx=10, pady=10, side="top")

        panel_teorema = ctk.CTkFrame(panel_texto, border_color="#4F769D", border_width=3)
        panel_teorema.pack(padx=10, pady=10, side="top")

        texto = "Para cada par de lenguajes L, L' con L ≤p L', si L es NP-Completo y L' es NP,\n" \
                "entonces el lenguaje L' es NP-Completo.\n" \

        label = ctk.CTkLabel(panel_teorema, text=texto)
        label.pack(padx=10, pady=10)

        texto = "En nuestro caso, aplicamos el teorema con L = HAMPATH (ya sabemos que \nes NP-Completo) " \
        "y L'= HAMCYCLE, así que concluimos que HAMCYCLE es \nNP-Completo."

        label = label = ctk.CTkLabel(panel_texto, text=texto)
        label.pack(padx=10, pady=10, side = "top")

        panel_botones_6 = ctk.CTkFrame(self.panel_2)
        panel_botones_6.pack(padx=10, pady=(0,10), fill=tk.Y, side='bottom')

        
        boton_anterior = ctk.CTkButton(panel_botones_6, text="Anterior", command=lambda:self.gestor_etapas.anterior(1))
        boton_anterior.grid(row=0, column=0, padx=(10,20), pady=10)

        boton_siguiente = ctk.CTkButton(panel_botones_6, text="Fin", command=lambda:self.gestor_etapas.siguiente(3))
        boton_siguiente.grid(row=0, column=1, padx=(20,10), pady=10)