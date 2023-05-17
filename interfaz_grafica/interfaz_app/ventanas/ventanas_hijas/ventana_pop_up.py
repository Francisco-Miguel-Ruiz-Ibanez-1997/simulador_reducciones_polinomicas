from .ventana_hija import VentanaHija

############################################################
# Clase que hereda de VentanaHija. Usaremos esta
# clase para mandar mensajes al usuario informativos,
# como mensajes de error, de selección de problemas, etc.
# Con estas ventanas no usaremos .mainloop(), por lo que 
# su método de destrucción de ventana no incluirá el método
# quit().
############################################################
class VentanaPopUp(VentanaHija):

    # Constructor.
    def __init__(self, ventana_padre):

        super().__init__(ventana_padre)
        self.resizable(0,0)
    
    # Método exit.
    def exit(self):

        self.destroy()