from .ventana_hija import VentanaHija

############################################################
# Clase que hereda de VentanaHija. Usaremos  principalmente
# esta clase como contenedor principal de la poli-reducción
# a realizar por el simulador.
# Con estas ventanas usaremos .mainloop(), por lo que 
# su método de destrucción de ventana incluirá el método
# quit().
###########################################################
class VentanaSecundaria(VentanaHija):

    # Constructor.
    def __init__(self, ventana_padre):

        super().__init__(ventana_padre)
    
    # Método exit.
    def exit(self):

        self.quit()
        self.destroy()