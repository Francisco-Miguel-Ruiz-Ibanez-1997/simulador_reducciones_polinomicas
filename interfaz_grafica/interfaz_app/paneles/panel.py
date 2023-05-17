import customtkinter as ctk

############################################################
# Panel representa el contenedor principal de la aplicación.
############################################################
class Panel(ctk.CTkFrame):

    # Constructor.
    def __init__(self, ventana=None):

        # Constructor del padre
        super().__init__(ventana, fg_color=("#98B3D0","gray16"), corner_radius=0)

        self.ventana = ventana
        self.pack(fill="both", expand=True)