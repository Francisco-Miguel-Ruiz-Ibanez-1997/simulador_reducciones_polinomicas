import tkinter as tk
from PIL import Image, ImageTk

import interfaz_grafica.interfaz_app.paneles as pn

##################################################
# Clase ventana que se abre encima de otra ventana
# padre. Hereda de tk.Toplevel.
##################################################
class VentanaHija(tk.Toplevel):

    # Constructor.
    def __init__(self, ventana_padre):

        # Constructor del padre
        super().__init__(ventana_padre)

        # Definición de protocolo al cerrar la ventana cuando
        # se pulsa X.
        self.protocol("WM_DELETE_WINDOW", lambda:self.exit())
    
    # Método para centrar una ventana.
    def center(self):
        """
        https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter
        """
        self.update_idletasks()
        width =  self.winfo_width()
        frm_width =  self.winfo_rootx() -  self.winfo_x()
        win_width = width + 2 * frm_width
        height =  self.winfo_height()
        titlebar_height =  self.winfo_rooty() -  self.winfo_y()
        win_height = height + titlebar_height + frm_width
        x =  self.winfo_screenwidth() // 2 - win_width // 2
        y =  self.winfo_screenheight() // 2 - win_height // 2
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        self.deiconify()
    
    # Método a ejecutar cuando se cierra la ventana. Las clases hijas
    # se encargarán de implementarlo.
    def exit():
        pass